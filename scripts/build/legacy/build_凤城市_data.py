#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 凤城市 (丹东市，辽宁省).

Investigation date: 2026-08-06
Task ID: liaoning_凤城市
Level: 县级市
Parent city: 丹东市
Targets: 市委书记 & 市长

Research status: PRIMARY SOURCE ACCESS (strong official coverage)
  - 凤城市人民政府门户网站 (www.lnfc.gov.cn): 可访问（凤城市融媒体中心一手报道）
  - 丹东市人民政府门户网站 (www.dandong.gov.cn): 可访问（县区动态栏目）
  - 现任市委书记 苗永鹏、市委副书记/市长 吴兆祎 已通过官方一手信源确认；
    凤城市第八次党代会（2026-07-29/30 换届）、第七届人民代表大会第六次会议
    （2026-07-17 选举吴兆祎为市长）等官方报道充分。
  - 四大班子、市委常委会成员、市政府副市长全名单均经官方一手报道确认。
  - Exa / Baidu / Bing / Sogou 检索普遍受限，核心领导出生年/籍贯/学历等履历
    细节仍缺失，按证据分级标注（current_role confirmed = 官方一手报道）。

Confirmed current officeholders (as of 2026-08-06):
   - 市委书记: 苗永鹏（多次官方调研报道；2026-07-17 主持第七届人代会六次会议、07-31 深入南部乡镇调研、08-04 常委会八届一次主持）
   - 市委副书记、市长: 吴兆祎（2026-07-17 第七届人大六次会议选举为凤城市人民政府市长，此前为代市长）
   - 市委副书记: 袁琦
   - 市委常委会: 组织部部长 邹研、纪委书记 刘晓华、宣传部长 肖丽芹、副市长 刘晓达、副市长 阚朝东、政法委书记 于福刚、统战部长 孙际超
   - 市人大常委会主任: 李永国；副主任: 曹会祥、王毓娥、杨德冲、王桂红
   - 市政协主席: 陈志华（2026-07-17 在任）；市政协党组书记 肖丽芹（2026-08-04 在任，兼宣传部长）
   - 市政府副市长: 姜晓峰（兼市公安局局长）、时红、丁威、潘晓宇、丛林
   - 市法院院长: 于丕健；市检察院检察长: 李丹

Predecessor timeline (piecemeal / unverified):
   - 市委书记: 苗永鹏 延续"七届→八届"（八届 2026-07-30 成立），前任书记及去向待核
   - 市长: 吴兆祎 由"代市长"（<=2026-07）转正，前任市长待核

Cross-region / context:
   - 凤城市 系丹东市代管的县级市，下辖 凤凰城街道、通远堡镇、青城子镇 等乡镇（街道）
   - 与丹东市辖 元宝/振兴/振安（市辖区）同属丹东市委干部管理体系，构成 市—县(市) 干部流动层
   - 丹东市委组织部 任前公示 为本区域干部来源依据（公开名单未见）

Confidence policy: 当前角色 confirmed（官方一手），身份(出生/籍贯/学历)与前任名字未确认。
"""

from __future__ import annotations

import json
import sys
import sqlite3
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

# ── Metadata ─────────────────────────────────────────────────────────────
SLUG = "凤城市"
TODAY_str = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"
PERSONS_STAGING_DIR = _CURRENT_DIR

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # ── 市委 ──
    {"id": 1, "name": "苗永鹏", "gender": "男", "ethnicity": "待查", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "", "current_post": "市委书记",
     "current_org": "中国共产党凤城市委员会",
     "source": "https://www.dandong.gov.cn/html/DDSZF/202608/0178580484107784.html (2026-08 凤城领导南部乡镇调研)"},
    {"id": 2, "name": "吴兆祎", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "", "current_post": "市委副书记、市长",
     "current_org": "凤城市人民政府",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html (2026-07-17 第七届人大六次会议选举)"},
    {"id": 3, "name": "袁琦", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "", "current_post": "市委副书记",
     "current_org": "中国共产党凤城市委员会",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html (2026-07-17 人代会六次会议)"},
    {"id": 4, "name": "邹研", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "", "current_post": "市委常委、组织部部长",
     "current_org": "中国共产党凤城市委员会",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/004450920478312.html (2026-07-20 市委组织部调研)"},
    {"id": 5, "name": "刘晓华", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "", "current_post": "市委常委、市纪委书记、市监委主任",
     "current_org": "中国共产党凤城市纪律检查委员会",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html (2026-07-17 人代会六次会议)"},
    {"id": 6, "name": "肖丽芹", "gender": "女", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "", "current_post": "市委常委、宣传部部长；市政协党组书记",
     "current_org": "中国共产党凤城市委员会",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html (2026-07-17 人代会六次会议，宣传部长)；https://www.lnfc.gov.cn/html/FCSZF/202608/006008847646714.html (2026-08-04 常委会八届一次，政协党组书记)"},
    {"id": 7, "name": "刘晓达", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "", "current_post": "市委常委、常务副市长",
     "current_org": "凤城市人民政府",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178512046390114.html (2026-07-23 消防慰问)"},
    {"id": 8, "name": "阚朝东", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "", "current_post": "市委常委、副市长",
     "current_org": "凤城市人民政府",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178512046390114.html (2026-07-23 消防慰问)"},
    {"id": 9, "name": "于福刚", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "", "current_post": "市委常委、政法委书记",
     "current_org": "中国共产党凤城市委员会",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html (2026-07-17 人代会六次会议)"},
    {"id": 10, "name": "孙际超", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "", "current_post": "市委常委、统战部部长",
     "current_org": "中国共产党凤城市委员会",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html (2026-07-17 人代会六次会议)"},
    # ── 人大 ──
    {"id": 11, "name": "李永国", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "", "current_post": "市人大常委会主任",
     "current_org": "凤城市人民代表大会常务委员会",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202608/00600884767622.html (2026-08-04 常委会八届一次)"},
    {"id": 12, "name": "纪家祥", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "", "current_post": "市人大常委会副主任",
     "current_org": "凤城市人民代表大会常务委员会",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html"},
    {"id": 13, "name": "王毓娥", "gender": "女", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "", "current_post": "市人大常委会副主任",
     "current_org": "凤城市人民代表大会常务委员会", "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html"},
    {"id": 14, "name": "杨德冲", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "", "current_post": "市人大常委会副主任",
     "current_org": "凤城市人民代表大会常务委员会", "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html"},
    {"id": 15, "name": "王桂红", "gender": "女", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "", "current_post": "市人大常委会副主任",
     "current_org": "凤城市人民代表大会常务委员会", "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html"},
    # ── 政协 ──
    {"id": 16, "name": "陈志华", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "", "current_post": "市政协主席",
     "current_org": "中国人民政治协商会议凤城市委员会",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html (2026-07-17)"},
    # ── 政府（副市长） ──
    {"id": 18, "name": "姜晓峰", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "", "current_post": "副市长、市公安局局长",
     "current_org": "凤城市人民政府",
     "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178440833991902.html (2026-07-06 安全生产部署会)"},
    {"id": 19, "name": "时红", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "", "current_post": "副市长",
     "current_org": "凤城市人民政府", "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178440833991902.html"},
    {"id": 20, "name": "丁威", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "", "current_post": "副市长",
     "current_org": "凤城市人民政府", "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178440833991902.html"},
    {"id": 21, "name": "丛林", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "", "current_post": "副市长",
     "current_org": "凤城市人民政府",
     "source": "https://www.dandong.gov.cn/html/DDSZF/202608/0178580484107784.html (2026-07-31 南部乡镇调研)"},
    {"id": 22, "name": "潘晓宇", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "", "current_post": "副市长",
     "current_org": "凤城市人民政府", "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178440833991902.html"},
    # ── 法检 ──
    {"id": 23, "name": "于丕健", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "", "current_post": "市人民法院院长",
     "current_org": "凤城市人民法院", "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html"},
    {"id": 24, "name": "李丹", "gender": "女", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "", "current_post": "市人民检察院检察长",
     "current_org": "凤城市人民检察院", "source": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html"},
]

organizations = [
    {"id": 1, "name": "中国共产党凤城市委员会", "type": "党委", "level": "县处级", "parent": "中共丹东市委", "location": "丹东市凤城市"},
    {"id": 2, "name": "凤城市人民政府", "type": "政府", "level": "县处级", "parent": "丹东市人民政府", "location": "丹东市凤城市"},
    {"id": 3, "name": "凤城市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "凤城市", "location": "丹东市凤城市"},
    {"id": 4, "name": "中国人民政治协商会议凤城市委员会", "type": "政协", "level": "县处级", "parent": "凤城市", "location": "丹东市凤城市"},
    {"id": 5, "name": "中国共产党凤城市纪律检查委员会/凤城市监察委员会", "type": "纪委", "level": "县处级", "parent": "中共丹东市纪委", "location": "丹东市凤城市"},
    {"id": 6, "name": "凤城市人民法院", "type": "法院", "level": "县处级", "parent": "丹东市中级人民法院", "location": "丹东市凤城市"},
    {"id": 7, "name": "凤城市人民检察院", "type": "检察院", "level": "县处级", "parent": "丹东市人民检察院", "location": "丹东市凤城市"},
    {"id": 8, "name": "凤城市公安局", "type": "政府", "level": "县处级", "parent": "凤城市人民政府", "location": "丹东市凤城市"},
    {"id": 9, "name": "中国共产党丹东市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委", "location": "丹东市"},
]

positions = [
    # 苗永鹏（市委书记）
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "<=2026", "end_date": "present", "rank": "县处级正职",
     "note": "2026-07 八届党代会后继续任书记；07-17 人代会并主持、07-31 南部乡镇调研、08-04 常委会八届一次主持"},
    {"person_id": 1, "org_id": 1, "title": "市委委员、市委常委", "start_date": "~2021-2026", "end_date": "present", "rank": "县处级",
     "note": "七届市委（2021-2026）任期内任书记并过渡至八届"},
    # 吴兆祎（2）
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "<=2026-07", "end_date": "present", "rank": "县处级正职",
     "note": "第七届人大六次会议（2026-07-17）选举为市长；此前为代市长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "<=2026-07", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 袁琦（3）副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "2026-07-31 调研陪同；2026-07-17 人代会前排"},
    # 邹研（4）组织部长
    {"person_id": 4, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "2026-07-16 市委组织部调研陪同"},
    # 刘晓华（5）纪委书记
    {"person_id": 5, "org_id": 5, "title": "市委常委、纪委书记、监委主任", "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": "2026-07-17 人代会六次会议主席台前排就座"},
    # 肖丽芹（6）宣传部长
    {"person_id": 6, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": "2026-07-17 人代会六次会议"},
    # 刘晓达（7）常务副市长
    {"person_id": 7, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "2026-07-23 消防慰问、07-28 矿山安全会主持"},
    # 阚朝东（8）
    {"person_id": 8, "org_id": 2, "title": "市委常委、副市长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "2026-07-23 消防慰问"},
    # 于福刚（9）
    {"person_id": 9, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    # 孙际超（10）
    {"person_id": 10, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    # 李永国（11）
    {"person_id": 11, "org_id": 3, "title": "市人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "2026-08-04 / 07-17 人代会主持"},
    # 人大副主任
    {"person_id": 12, "org_id": 3, "title": "市人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "市人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "市人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "市人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 陈志华（16）政协主席；肖丽芹（6）政协党组书记（亦为市委常委、宣传部长）
    {"person_id": 16, "org_id": 4, "title": "市政协主席", "start_date": "unknown", "end_date": "~2026-07", "rank": "县处级正职", "note": "2026-07-17 人代会确认"},
    {"person_id": 6, "org_id": 4, "title": "市政协党组书记", "start_date": "~2026-08", "end_date": "present", "rank": "县处级正职", "note": "2026-08-04 常委会八届一次在任"},
    # 政府副市长
    {"person_id": 18, "org_id": 8, "title": "副市长、市公安局局长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    # 法检
    {"person_id": 23, "org_id": 6, "title": "市人民法院院长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 24, "org_id": 7, "title": "市人民检察院检察长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
]

relationships = [
    # 核心党政搭档
    {"person_a": 1, "person_b": 2, "type": "co_leadership", "context": "市委书记与市长（市长兼市委副书记）——党政一把手搭班",
     "overlap_org": "凤城市", "overlap_period": "2026-", "confidence": "confirmed"},
    # 四大班子互关
    {"person_a": 1, "person_b": 11, "type": "co_leadership", "context": "市委书记与市人大常委会主任（八届一次常委会同台）", "overlap_org": "凤城市", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 16, "type": "co_leadership", "context": "市委书记与市政协主席（人代会六次会议同台）", "overlap_org": "凤城市", "overlap_period": "2026-07", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "co_leadership", "context": "市委书记与市政协党组书记/宣传部长（八届一次常委会同台）", "overlap_org": "凤城市", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "co_leadership", "context": "市长（代转正）与人大主任（人代会六次会议选举）", "overlap_org": "凤城市人大常委会", "overlap_period": "2026-07", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "co_leadership", "context": "市长与政协主席（人代会同台）", "overlap_org": "凤城市", "overlap_period": "2026-07", "confidence": "confirmed"},
    # 市委班子：副书记、纪委、宣传、政法、统战
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记与副书记（干部队伍、党建共同部署）", "overlap_org": "凤城市委", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "书记与组织部长（组织部调研，抓组织/干部/党建）", "overlap_org": "凤城市委组织部", "overlap_period": "2026-07", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "co_leadership", "context": "书记与纪委书记（人代会前排同台）", "overlap_org": "凤城市", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "co_leadership", "context": "书记与常务副市长（消防慰问、南部调研同台）", "overlap_org": "凤城市", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长与常务副市长（市政府班子、矿山安全生产会）", "overlap_org": "凤城市人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate", "context": "市长分管公安（安全生产部署会）", "overlap_org": "凤城市人民政府", "overlap_period": "2026-07", "confidence": "confirmed"},
    # 政府班子互为同事
    {"person_a": 7, "person_b": 8, "type": "co_leadership", "context": "市委常委/副市长（政府班子）", "overlap_org": "凤城市人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 18, "person_b": 19, "type": "co_leadership", "context": "副市长同班子", "overlap_org": "凤城市人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 20, "person_b": 21, "type": "co_leadership", "context": "副市长同班子", "overlap_org": "凤城市人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 21, "person_b": 22, "type": "co_leadership", "context": "副市长同班子", "overlap_org": "凤城市人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
]


# ── Person JSONs ────────────────────────────────────────────────────────
def write_person_jsons():
    """Write per-person graph JSON for the two core leaders (市委书记 & 市长)."""

    miao = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "丹东市", "region": "凤城市",
                                "job": "市委书记", "task_id": "liaoning_凤城市", "time_focus": "2025-2026"},
        "identity": {
            "person_id": "dandong_fengcheng_miaoyonglin",
            "name": "苗永鹏",
            "aliases": [],
            "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "", "native_place": "",
            "education": [{"period": "", "institution": "待查", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "苗永鹏_unknown", "name_birthplace": "苗永鹏_unknown",
                            "official_profile_url": "https://www.dandong.gov.cn/html/DDS/202608/0178580484100108.html"},
        },
        "current_status": {"current_post": "市委书记", "current_org": "中国共产党凤城市委员会",
                           "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S001", "S002", "S003"]},
        "career_timeline": [
            {"start": "~2021-2026", "end": "present", "org": "中共凤城市委员会", "title": "市委书记（七届→八届）",
             "level": "县处级", "location": "凤城市", "system": "party", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "2026-07-29~30 市第八次党代会、07-17 人代会讲话、08-04 常委会八届一次主持；换届延续任书记",
             "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任凤城市委书记之前（出生、籍贯、学历、入党、工作起始、此前职务）公开资料未检索到",
             "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "中国共产党凤城市委员会", "role": "市委书记"}],
        "relationships": [
            {"person": "吴兆祎", "person_id": "dandong_fengcheng_wuzhaoyi", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：市委书记+市长", "overlap_org": "凤城市",
             "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
            {"person": "李永国", "person_id": "dandong_fengcheng_liyongguo", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "同届市领导（人大主任）", "overlap_org": "凤城市", "overlap_period": "2026-",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance_record": [
            {"period": "2026-07", "domain": "rural_revitalization", "achievement_or_event": "深入南部乡镇（红旗、蓝旗、沙里寨）调研民生基础设施、村集体经济发展、汛期安全、生态旅游整改",
             "role_in_event": "市委书记带队", "measurable_outcome": "", "location": "凤城市",
             "confidence": "confirmed", "source_ids": ["S002"]},
            {"period": "2026-07", "domain": "party_building", "achievement_or_event": "到市委组织部调研，部署市第八次党代会、抓党建促乡村振兴、干部选拔任用三标准",
             "role_in_event": "市委书记", "measurable_outcome": "", "location": "凤城市",
             "confidence": "confirmed", "source_ids": ["S004"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": ["party", "organization"],
            "geographic_pattern": [], "promotion_velocity": {"summary": "市委书记（现职），初始履历未知", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "grassroots_oriented", "evidence": "多次深入乡镇街道、防汛一线督导、走访居民家庭", "confidence": "plausible", "source_ids": ["S002", "S004"]}
            ],
            "speech_themes": ["民生保障", "乡村振兴", "防汛安全", "政绩观", "选人用人三标准"],
            "management_signals": [], "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-06未发现违纪或负面舆情", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "凤城市委常委会召开八届第一次会议", "url": "https://www.lnfc.gov.cn/html/FCSZF/202608/00600884768222.html",
             "publisher": "凤城市融媒体中心", "published_at": "2026-08-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "确认苗永鹏为市委书记"},
            {"id": "S002", "title": "凤城市领导深入南部乡镇调研民生发展、集体经济与防汛安全等重点工作", "url": "https://www.dandong.gov.cn/html/DDSZF/202608/0178580484107784.html",
             "publisher": "丹东市网/凤城市融媒体中心", "published_at": "2026-08-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "2026-07-31 苗永鹏率袁琦、邹研、丛林调研"},
            {"id": "S003", "title": "凤城市第七届人民代表大会第六次会议召开", "url": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html",
             "publisher": "凤城市融媒体中心", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "苗永鹏、吴兆祎、袁琦等市领导在任确认"},
            {"id": "S004", "title": "凤城市领导到凤城市委组织部调研", "url": "https://www.lnfc.gov.cn/html/FCSZF/202607/004450920478312.html",
             "publisher": "凤城市融媒体中心", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "苗永鹏组织繁殖建设"},
        ],
        "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "苗永鹏完整履历与姓名细节"},
        "open_questions": [
            {"priority": "critical", "question": "苗永鹏出生年月、籍贯、教育背景、入党时间、参加工作时间", "why_it_matters": "基本身份信息缺失",
             "suggested_queries": ["苗永鹏 简历 凤城 丹东"], "last_attempted": AS_OF},
            {"priority": "high", "question": "苗永鹏何时何地调任凤城市委书记、任前职务", "why_it_matters": "判断干部交流源头",
             "suggested_queries": ["苗永鹏 任前公示 丹东"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "前任市委书记/市长去向、市委市政府换届交接时间", "why_it_matters": "判断班子延续",
             "suggested_queries": ["凤城市 市委 换届 前任"], "last_attempted": AS_OF},
        ],
    }

    wu = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "丹东市", "region": "凤城市",
                                "job": "市长", "task_id": "liaoning_凤城市", "time_focus": "2025-2026"},
        "identity": {
            "person_id": "dandong_fengcheng_wuzhaoyi",
            "name": "吴兆祎",
            "aliases": [],
            "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "", "native_place": "",
            "education": [{"period": "", "institution": "待查", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "吴兆祎_unknown", "name_birthplace": "吴兆祎_unknown",
                            "official_profile_url": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html"},
        },
        "current_status": {"current_post": "市委副书记、市长", "current_org": "凤城市人民政府",
                           "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S001", "S002"]},
        "career_timeline": [
            {"start": "<=2026-07", "end": "present", "org": "凤城市人民政府", "title": "市长",
             "level": "县处级", "location": "凤城市", "system": "government", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "第七届人大六次会议2026-07-17无记名投票选举为市长（曾任代市长），依法宣誓",
             "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "<=2026-07", "end": "present", "org": "中共凤城市委员会", "title": "市委副书记",
             "level": "县处级", "location": "凤城市", "system": "party", "rank": "县处级正职", "is_key_promotion": False,
             "notes": "市长党内职", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任代市长/市长前及更早履历（出生、籍贯、学历、此前职务）公开资料缺失", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "凤城市人民政府", "role": "市长"}],
        "relationships": [
            {"person": "苗永鹏", "person_id": "dandong_fengcheng_miaoyonglin", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：市长（代转正）与书记", "overlap_org": "凤城市", "overlap_period": "2026-",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
            {"person": "李永国", "person_id": "dandong_fengcheng_liyongguo", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "市长当选由人大主任主持全体会议", "overlap_org": "凤城市人大常委会", "overlap_period": "2026-07",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance_record": [
            {"period": "2026-07", "domain": "public_security", "achievement_or_event": "主持矿山安全生产工作会议，部署治本攻坚、汛期矿山安全",
             "role_in_event": "市长（兼市委副书记）", "measurable_outcome": "", "location": "凤城市", "confidence": "confirmed", "source_ids": ["S004"]},
            {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "就职表态：优化营商环境一把手工程、'十五五'规划目标、对外开放",
             "role_in_event": "市长", "measurable_outcome": "", "location": "凤城市", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": ["government"],
            "geographic_pattern": [], "promotion_velocity": {"summary": "由代市长转正为市长", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "pragmatic", "evidence": "主抓安全生产、营商环境、'十五五'规划落实", "confidence": "plausible", "source_ids": ["S001", "S004"]}
            ],
            "speech_themes": ["营商环境", "高质量发展", "安全生产", "法治政府"],
            "management_signals": [], "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-06未发现违纪或负面舆情", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "凤城市第七届人民代表大会第六次会议召开", "url": "https://www.lnfc.gov.cn/html/FCSZF/202607/0178453141770844.html",
             "publisher": "凤城市融媒体中心", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "吴兆祎当选市长、依法宣誓与表态"},
            {"id": "S002", "title": "凤城市委常委会召开八届委员会第一次会议", "url": "https://www.lnfc.gov.cn/html/FCSZF/202608/00600884768222.html",
             "publisher": "凤城市融媒体中心", "published_at": "2026-08-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "吴兆祎以市委副书记、市长身份出席"},
            {"id": "S003", "title": "凤城市领导深入南部乡镇调研", "url": "https://www.dandong.gov.cn/html/DDSZF/202608/017850484107784.html",
             "publisher": "丹东市网", "published_at": "2026-08-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "苗永鹏、吴兆祎同台出席"},
            {"id": "S004", "title": "凤城市召开矿山安全生产工作会议", "url": "https://www.lnfc.gov.cn/html/FCSZF/202607/00428528613726995.html",
             "publisher": "凤城市融媒体中心", "published_at": "2026-07-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "吴兆祎讲话"},
        ],
        "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "吴兆祎任市长前完整履历（出生/籍贯/学历/此前职务/任期起始）"},
        "open_questions": [
            {"priority": "critical", "question": "吴兆祎出生年月、籍贯、教育背景、入党时间、此前职务", "why_it_matters": "基本身份信息与晋升轨迹",
             "suggested_queries": ["吴兆祎 简历 凤城 丹东"], "last_attempted": AS_OF},
            {"priority": "high", "question": "吴兆祎何时调任凤城任代市长；任前职务", "why_it_matters": "判断干部来源",
             "suggested_queries": ["吴兆祎 代市长 任职"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "市政府其他副市长分工与常务副市长的在任时间", "why_it_matters": "政府班子结构",
             "suggested_queries": ["凤城市 副市长 名单"], "last_attempted": AS_OF},
        ],
    }

    person_dir = PERSONS_STAGING_DIR
    today = AS_OF.replace("-", "")
    for fname, data in [
        (f"{today}-辽宁省-丹东市-市委书记-苗永鹏.json", miao),
        (f"{today}-辽宁省-丹东市-市长-吴兆祎.json", wu),
    ]:
        path = person_dir / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")


def main():
    print(f"Building {SLUG} network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    write_person_jsons()

    print(f"\nDone! Staged output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    for f in sorted(PERSONS_STAGING_DIR.glob("*.json")):
        if "凤城" in f.name:
            print(f"  JSON: {f}")


if __name__ == "__main__":
    main()