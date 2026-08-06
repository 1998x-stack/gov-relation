#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 伍家岗区 (Wujiagang District), 宜昌市, 湖北省.

Level: 市辖区
Province: 湖北省
Parent city: 宜昌市
Targets: 区委书记 (Party Secretary), 区长 (District Governor)
Task ID: hubei_伍家岗区

Research date: 2026-08-06
Official source: http://www.ycwjg.gov.cn/ (伍家岗区人民政府) — confirmed accessible

Current status (as of 2026-08-06):
- 区委书记: 陈道坤 (confirmed via official 区委领导 page + 时政要闻 news, e.g. 区委理论学习中心组 2026-07-22)
- 区委副书记、区长、工业园区党工委书记: 吴晓军 (confirmed via official 区委/区政府领导 pages + news 2026-07-29)

Roster sources:
  区委领导: http://www.ycwjg.gov.cn/pcms_611_lingdaozhichuang_13/pcms_611_quweilingdao_14.html
  区政府领导: http://www.ycwjg.gov.cn/pcms_611_lingdaozhichuang_13/pcms_611_quzhengfulingdao_17.html
  区人大领导: http://www.ycwjg.gov.cn/pcms_611_lingdaozhichuang_13/pcms_611_qurendalingdao_15.html
  区政协领导: http://www.ycwjg.gov.cn/pcms_611_lingdaozhichuang_13/pcms_611_quzhengxielingdao_16.html

Confidence notes:
- Current roles and identity fields (gender, ethnicity, birth, education) for all 区委/人大/政府/政协
  leaders: confirmed via official personal bio entries (2026-08)
- Position duty scopes (分工) for 区政府 deputy mayors: confirmed via official 区政府领导页
- Full PRIOR career-timeline segments (posts before current role): unverified (official bio gives only
  identity + current role). Career histories for 陈道坤/吴晓军 being filled by research agents; encode gaps.
- Predecessor 书记/区长 identities and tenures: unverified under degraded web access — see open gaps.
- All birth years gendered/data from official site only; no fabrication.
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
SLUG = "伍家岗区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

def repo_root(start: Path) -> Path:
    cur = start
    while cur != cur.parent:
        if (cur / "gov_relation").is_dir():
            return cur
        cur = cur.parent
    return start

BASE = repo_root(SCRIPT_DIR)
DB_PATH = BASE / "data" / "database" / f"{SLUG}_network.db"
GEXF_PATH = BASE / "data" / "graph" / f"{SLUG}_network.gexf"

# Core source URIs reused throughout
S_QW = "http://www.ycwjg.gov.cn/pcms_611_lingdaozhichuang_13/pcms_611_quweilingdao_14.html"
S_QZF = "http://www.ycwjg.gov.cn/pcms_611_lingdaozhichuang_13/pcms_611_quzhengfulingdao_17.html"
S_QRD = "http://www.ycwjg.gov.cn/pcms_611_lingdaozhichuang_13/pcms_611_qurendalingdao_15.html"
S_QZX = "http://www.ycwjg.gov.cn/pcms_611_lingdaozhichuang_13/pcms_611_quzhengxielingdao_16.html"
S_NEWS = "http://www.ycwjg.gov.cn/pcms_611_wujiazixun_18/pcms_611_wujiayaowen_19.html"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "陈道坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-04",
        "birthplace": "",
        "education": "在职党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共宜昌市伍家岗区委员会",
        "source": S_QW,
    },
    {
        "id": 2,
        "name": "吴晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-10",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长、工业园区党工委书记",
        "current_org": "伍家岗区人民政府",
        "source": S_QZF,
    },
    {
        "id": 3,
        "name": "高大权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-04",
        "birthplace": "",
        "education": "全日制硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共宜昌市伍家岗区委员会",
        "source": S_QW,
    },
    # ═══════ 区委领导 ═══════
    {
        "id": 4,
        "name": "刘政学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-07",
        "birthplace": "",
        "education": "大学、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共宜昌市伍家岗区委政法委员会",
        "source": S_QW,
    },
    {
        "id": 5,
        "name": "王凤兰",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1976-12",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共宜昌市伍家岗区纪律检查委员会",
        "source": S_QW,
    },
    {
        "id": 6,
        "name": "张杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-06",
        "birthplace": "",
        "education": "大学、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长、统战部部长，区政协党组副书记",
        "current_org": "中共宜昌市伍家岗区委组织部",
        "source": S_QW,
    },
    {
        "id": 7,
        "name": "谢军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-02",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区委办公室主任、直属机关工委书记",
        "current_org": "中共宜昌市伍家岗区委办公室",
        "source": S_QW,
    },
    {
        "id": 8,
        "name": "汪伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-12",
        "birthplace": "",
        "education": "研究生、工学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府副区长（常务）、党组副书记",
        "current_org": "伍家岗区人民政府",
        "source": S_QZF,
    },
    {
        "id": 9,
        "name": "朱国锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-10",
        "birthplace": "",
        "education": "全日制大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区人武部上校部长",
        "current_org": "宜昌市伍家岗区人民武装部",
        "source": S_QW,
    },
    {
        "id": 10,
        "name": "杨凡",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1982-03",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长、区政府副区长",
        "current_org": "中共宜昌市伍家岗区委宣传部",
        "source": S_QZF,
    },
    # ═══════ 区政府其他领导 ═══════
    {
        "id": 11,
        "name": "李宏智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-06",
        "birthplace": "",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区公安分局党委书记、局长，区委政法委第一副书记",
        "current_org": "伍家岗公安分局",
        "source": S_QZF,
    },
    {
        "id": 12,
        "name": "张琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-08",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "无党派人士",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "伍家岗区人民政府",
        "source": S_QZF,
    },
    {
        "id": 13,
        "name": "陈莹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987-10",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "伍家岗区人民政府",
        "source": S_QZF,
    },
    {
        "id": 14,
        "name": "张海凌",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1978-09",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "伍家岗区人民政府",
        "source": S_QZF,
    },
    {
        "id": 15,
        "name": "赵翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-07",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "伍家岗区人民政府",
        "source": S_QZF,
    },
    {
        "id": 16,
        "name": "方正",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-05",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（挂职两年）",
        "current_org": "伍家岗区人民政府",
        "source": S_QZF,
    },
    # ═══════ 区人大常委会领导 ═══════
    {
        "id": 17,
        "name": "张友兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-11",
        "birthplace": "",
        "education": "全日制大学、在职公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任、党组书记",
        "current_org": "伍家岗区人民代表大会常务委员会",
        "source": S_QRD,
    },
    {
        "id": 18,
        "name": "杨燕军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-09",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任、党组副书记",
        "current_org": "伍家岗区人民代表大会常务委员会",
        "source": S_QRD,
    },
    {
        "id": 19,
        "name": "汪鸿波",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971-11",
        "birthplace": "",
        "education": "在职党校研究生",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "伍家岗区人民代表大会常务委员会",
        "source": S_QRD,
    },
    {
        "id": 20,
        "name": "段绪卿",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1972-11",
        "birthplace": "",
        "education": "在职党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任、党组成员，区总工会主席",
        "current_org": "伍家岗区人民代表大会常务委员会",
        "source": S_QRD,
    },
    {
        "id": 21,
        "name": "王华",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1973-12",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任、党组成员",
        "current_org": "伍家岗区人民代表大会常务委员会",
        "source": S_QRD,
    },
    {
        "id": 22,
        "name": "齐运建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-07",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任、党组成员",
        "current_org": "伍家岗区人民代表大会常务委员会",
        "source": S_QRD,
    },
    {
        "id": 23,
        "name": "湛保华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-04",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任、党组成员",
        "current_org": "伍家岗区人民代表大会常务委员会",
        "source": S_QRD,
    },
    # ═══════ 区政协领导 ═══════
    {
        "id": 24,
        "name": "熊晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-05",
        "birthplace": "",
        "education": "大学、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席、党组书记",
        "current_org": "中国人民政治协商会议宜昌市伍家岗区委员会",
        "source": S_QZX,
    },
    {
        "id": 25,
        "name": "张革会",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-02",
        "birthplace": "",
        "education": "在职党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席、党组副书记",
        "current_org": "中国人民政治协商会议宜昌市伍家岗区委员会",
        "source": S_QZX,
    },
    {
        "id": 26,
        "name": "周舟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-10",
        "birthplace": "",
        "education": "大学、工学学士",
        "party_join": "无党派人士",
        "work_start": "",
        "current_post": "区政协副主席、区工商联主席",
        "current_org": "中国人民政治协商会议宜昌市伍家岗区委员会",
        "source": S_QZX,
    },
    {
        "id": 27,
        "name": "宋玉彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-03",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席、党组成员",
        "current_org": "中国人民政治协商会议宜昌市伍家岗区委员会",
        "source": S_QZX,
    },
    {
        "id": 28,
        "name": "杨培新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "",
        "education": "大学、经济学学士",
        "party_join": "民建会员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议宜昌市伍家岗区委员会",
        "source": S_QZX,
    },
    {
        "id": 29,
        "name": "杜平",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970-03",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "民进会员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议宜昌市伍家岗区委员会",
        "source": S_QZX,
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共宜昌市伍家岗区委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市委员会", "location": "湖北省宜昌市伍家岗区"},
    {"id": 2, "name": "伍家岗区人民政府", "type": "政府", "level": "县级", "parent": "宜昌市人民政府", "location": "湖北省宜昌市伍家岗区"},
    {"id": 3, "name": "湖北伍家岗工业园区", "type": "开发区", "level": "县级", "parent": "伍家岗区人民政府", "location": "湖北省宜昌市伍家岗区"},
    {"id": 4, "name": "中共宜昌市伍家岗区委政法委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市伍家岗区委员会", "location": "湖北省宜昌市伍家岗区"},
    {"id": 5, "name": "中共宜昌市伍家岗区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市纪律检查委员会", "location": "湖北省宜昌市伍家岗区"},
    {"id": 6, "name": "伍家岗区监察委员会", "type": "党委", "level": "县级", "parent": "宜昌市监察委员会", "location": "湖北省宜昌市伍家岗区"},
    {"id": 7, "name": "中共宜昌市伍家岗区委组织部", "type": "党委", "level": "县级", "parent": "中共宜昌市伍家岗区委员会", "location": "湖北省宜昌市伍家岗区"},
    {"id": 8, "name": "中共宜昌市伍家岗区委统一战线工作部", "type": "党委", "level": "县级", "parent": "中共宜昌市伍家岗区委员会", "location": "湖北省宜昌市伍家岗区"},
    {"id": 9, "name": "中共宜昌市伍家岗区委宣传部", "type": "党委", "level": "县级", "parent": "中共宜昌市伍家岗区委员会", "location": "湖北省宜昌市伍家岗区"},
    {"id": 10, "name": "中共宜昌市伍家岗区委办公室", "type": "党委", "level": "县级", "parent": "中共宜昌市伍家岗区委员会", "location": "湖北省宜昌市伍家岗区"},
    {"id": 11, "name": "宜昌市伍家岗区人民武装部", "type": "党委", "level": "县级", "parent": "宜昌军分区", "location": "湖北省宜昌市伍家岗区"},
    {"id": 12, "name": "伍家岗公安分局", "type": "政府", "level": "县级", "parent": "宜昌市公安局", "location": "湖北省宜昌市伍家岗区"},
    {"id": 13, "name": "伍家岗区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "宜昌市人大常委会", "location": "湖北省宜昌市伍家岗区"},
    {"id": 14, "name": "中国人民政治协商会议宜昌市伍家岗区委员会", "type": "政协", "level": "县级", "parent": "政协宜昌市委员会", "location": "湖北省宜昌市伍家岗区"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "正县级", "note": "Confirmed as of 2026-08-06"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "正县级", "note": "Confirmed; 党组书记"},
    {"person_id": 2, "org_id": 3, "title": "工业园区党工委书记", "start": "", "end": "present", "rank": "正县级", "note": "湖北伍家岗工业园区党工委书记"},
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 区委领导
    {"person_id": 4, "org_id": 4, "title": "区委常委、政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "区委常委、纪委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "监委主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "区委常委、组织部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "统战部长", "start": "", "end": "present", "rank": "副县级", "note": "兼任区政协党组副书记"},
    {"person_id": 7, "org_id": 10, "title": "区委常委、区委办公室主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "区委常委、常务副区长", "start": "", "end": "present", "rank": "副县级", "note": "党组副书记"},
    {"person_id": 9, "org_id": 11, "title": "区委常委、人武部部长", "start": "", "end": "present", "rank": "副县级", "note": "上校"},
    {"person_id": 10, "org_id": 9, "title": "区委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": "党组成员"},
    # 区政府其他领导
    {"person_id": 11, "org_id": 12, "title": "副区长、区公安分局局长", "start": "", "end": "present", "rank": "副县级", "note": "区委政法委第一副书记"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": "无党派人士"},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": "党组成员"},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": "党组成员"},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": "党组成员"},
    {"person_id": 16, "org_id": 2, "title": "副区长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "挂职两年，博士"},
    # 人大
    {"person_id": 17, "org_id": 13, "title": "区人大常委会主任、党组书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 18, "org_id": 13, "title": "区人大常委会副主任、党组副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 19, "org_id": 13, "title": "区人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": "民盟"},
    {"person_id": 20, "org_id": 13, "title": "区人大常委会副主任、党组成员", "start": "", "end": "present", "rank": "副县级", "note": "区总工会主席"},
    {"person_id": 21, "org_id": 13, "title": "区人大常委会副主任、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 22, "org_id": 13, "title": "区人大常委会副主任、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 23, "org_id": 13, "title": "区人大常委会副主任、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 政协
    {"person_id": 24, "org_id": 14, "title": "区政协主席、党组书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 25, "org_id": 14, "title": "区政协副主席、党组副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 26, "org_id": 14, "title": "区政协副主席、区工商联主席", "start": "", "end": "present", "rank": "副县级", "note": "无党派"},
    {"person_id": 27, "org_id": 14, "title": "区政协副主席、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 28, "org_id": 14, "title": "区政协副主席", "start": "", "end": "present", "rank": "副县级", "note": "民建"},
    {"person_id": 29, "org_id": 14, "title": "区政协副主席", "start": "", "end": "present", "rank": "副县级", "note": "民进"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长党政主要领导搭档，共同主持区委常委会、理论学习中心组等（2026-07-22）", "overlap_org": "伍家岗区", "overlap_period": "current"},
    # 区委书记 与 区委班子成员
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与区委副书记", "overlap_org": "中共宜昌市伍家岗区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与政法委书记", "overlap_org": "中共宜昌市伍家岗区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与纪委书记", "overlap_org": "中共宜昌市伍家岗区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与组织部部长", "overlap_org": "中共宜昌市伍家岗区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记与区委办主任", "overlap_org": "中共宜昌市伍家岗区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记与常务副区长（皆为区委常委）", "overlap_org": "中共宜昌市伍家岗区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记与宣传部部长/副区长", "overlap_org": "中共宜昌市伍家岗区委员会", "overlap_period": "current"},
    # 区长 与 政府班子
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与常务副区长", "overlap_org": "伍家岗区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "伍家岗区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "区长与副区长/公安局长", "overlap_org": "伍家岗区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "伍家岗区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "伍家岗区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "伍家岗区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "伍家岗区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "区长与挂职副区长（博士援派）", "overlap_org": "伍家岗区人民政府", "overlap_period": "current"},
    # 政法系统联动
    {"person_a": 4, "person_b": 11, "type": "overlap", "context": "政法委书记与公安局长（政法系统联动，公安局长兼政法委第一副书记）", "overlap_org": "伍家岗区政法系统", "overlap_period": "current"},
    # 组织系统：组织部长 与 区委书记（干部任用）
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与组织部部长（干部任用主线）", "overlap_org": "中共宜昌市伍家岗区委员会", "overlap_period": "current"},
    # 人大主任/政协主席 与 区委书记（四套班子）
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "区委书记与区人大常委会主任（四套班子协同）", "overlap_org": "伍家岗区", "overlap_period": "current"},
    {"person_a": 1, "person_b": 24, "type": "overlap", "context": "区委书记与区政协主席（四套班子协同）", "overlap_org": "伍家岗区", "overlap_period": "current"},
]

sys.path.insert(0, str(BASE))
try:
    import sqlite3  # noqa: F811

    # ── Inject repo path & use the runner (fallback to standalone below) ──
    from gov_relation.runner import run_build

    print(f"=== Building {SLUG} network ===")
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

    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("=== Done ===")

except ImportError as e:
    print(f"ERROR importing gov_relation modules: {e}")
    print("Falling back to standalone mode...")
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
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
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        conn.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p.get("education", ""), p["party_join"], p.get("work_start", ""),
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        conn.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        conn.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""),
              pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        conn.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"Standalone DB written: {DB_PATH}")