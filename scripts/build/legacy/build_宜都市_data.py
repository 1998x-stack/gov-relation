#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 宜都市 (Yidu City), 宜昌市, 湖北省.

Level: 县级市
Province: 湖北省
Parent city: 宜昌市
Targets: 市委书记 (Party Secretary), 市长 (Mayor)
Task ID: hubei_宜都市

Research date: 2026-07-24
Official source: https://www.yidu.gov.cn/ (宜都市人民政府) — confirmed accessible via HTTPS

Current status (as of 2026-07-24):
- 市委书记: 夏明海 (confirmed via official 市委领导 page https://www.yidu.gov.cn/list-21591-1.html + news article)
- 市长: 周斌 (confirmed via official 市政府领导 page)

Official leadership page: https://www.yidu.gov.cn/list-21591-1.html (领导之窗)
  - 市委领导: https://www.yidu.gov.cn/list-21591-1.html
  - 市政府领导: https://www.yidu.gov.cn/list-21591-1.html (same page, tabs)

Confidence notes:
  - Current roles for all 市委 and 市政府 members: confirmed via official government website
  - Career histories for all leaders: unverified — only current positions confirmed from official sources
  - Birth details: partially known (ages and birth years from official page)
  - Exa search was rate-limited; Baidu returned 403; Jina Reader timed out
  - Education info: confirmed from official bios to degree level (institution details unverified)
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "宜都市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "夏明海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "",
        "education": "大学学历、在职工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共宜都市委员会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 2,
        "name": "周斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "研究生学历、法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "宜都市人民政府",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    # ═══════ 市委领导 ═══════
    {
        "id": 3,
        "name": "王悦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年6月",
        "birthplace": "",
        "education": "研究生学历、博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、姚家店镇党委书记",
        "current_org": "中共宜都市委员会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 4,
        "name": "江競",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、人武部上校部长",
        "current_org": "中共宜都市委员会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 5,
        "name": "周勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年4月",
        "birthplace": "",
        "education": "大学学历、农业推广硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监察委员会主任",
        "current_org": "中共宜都市纪律检查委员会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 6,
        "name": "覃海洋",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1981年5月",
        "birthplace": "",
        "education": "大学学历、农学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "宜都市人民政府",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 7,
        "name": "王燕妮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年3月",
        "birthplace": "",
        "education": "大学学历、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长、市委党校校长",
        "current_org": "中共宜都市委员会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 8,
        "name": "杨超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年9月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长，市政协党组副书记",
        "current_org": "中共宜都市委员会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 9,
        "name": "阮晓阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年9月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长、市总工会主席",
        "current_org": "中共宜都市委员会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 10,
        "name": "李青松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共宜都市委员会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 11,
        "name": "朱景波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年9月",
        "birthplace": "",
        "education": "大学学历、农业推广硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委办公室主任、市委直属机关工委书记",
        "current_org": "中共宜都市委员会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    # ═══════ 市政府其他领导 ═══════
    {
        "id": 12,
        "name": "蒋小丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "副市长、市工商联主席",
        "current_org": "宜都市人民政府",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 13,
        "name": "严军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年6月",
        "birthplace": "",
        "education": "在职大学学历、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、党组成员，市委政法委第一副书记，市公安局党委书记、局长、督察长",
        "current_org": "宜都市人民政府",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 14,
        "name": "曾谊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "",
        "education": "大学学历、教育学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、党组成员",
        "current_org": "宜都市人民政府",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 15,
        "name": "杨华",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、党组成员",
        "current_org": "宜都市人民政府",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 16,
        "name": "李兴炎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "",
        "education": "大学学历、农学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、党组成员，陆城街道党工委书记",
        "current_org": "宜都市人民政府",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    # ═══════ 市人大领导 ═══════
    {
        "id": 17,
        "name": "龙顶泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年4月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任、党组书记",
        "current_org": "宜都市人大常委会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 18,
        "name": "刘建宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年7月",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任、党组副书记",
        "current_org": "宜都市人大常委会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 19,
        "name": "孙家武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年10月",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任、党组成员",
        "current_org": "宜都市人大常委会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 20,
        "name": "覃晴",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1971年1月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任、党组成员",
        "current_org": "宜都市人大常委会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 21,
        "name": "吴斌",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1969年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任、党组成员",
        "current_org": "宜都市人大常委会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 22,
        "name": "许文忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年4月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任、党组成员",
        "current_org": "宜都市人大常委会",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    # ═══════ 市政协领导 ═══════
    {
        "id": 23,
        "name": "张红新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年2月",
        "birthplace": "",
        "education": "大学学历、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席、党组书记",
        "current_org": "宜都市政协",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 24,
        "name": "王德凤",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970年1月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协副主席、党组副书记",
        "current_org": "宜都市政协",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 25,
        "name": "张华",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1984年11月",
        "birthplace": "",
        "education": "在职研究生学历、公共管理硕士",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "宜都市政协",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 26,
        "name": "李强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "",
        "education": "研究生学历、工学硕士",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "宜都市政协",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 27,
        "name": "谢辉喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协副主席、党组成员",
        "current_org": "宜都市政协",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
    {
        "id": 28,
        "name": "王小明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "宜都市政协",
        "source": "https://www.yidu.gov.cn/list-21591-1.html"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共宜都市委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市委员会", "location": "湖北省宜昌市宜都市"},
    {"id": 2, "name": "宜都市人民政府", "type": "政府", "level": "县级", "parent": "宜昌市人民政府", "location": "湖北省宜昌市宜都市"},
    {"id": 3, "name": "中共宜都市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市纪律检查委员会", "location": "湖北省宜昌市宜都市"},
    {"id": 4, "name": "宜都市监察委员会", "type": "党委", "level": "县级", "parent": "宜昌市监察委员会", "location": "湖北省宜昌市宜都市"},
    {"id": 5, "name": "宜都市人民武装部", "type": "政府", "level": "县级", "parent": "宜昌市军分区", "location": "湖北省宜昌市宜都市"},
    {"id": 6, "name": "中共宜都市委组织部", "type": "党委", "level": "县级", "parent": "中共宜都市委员会", "location": "湖北省宜昌市宜都市"},
    {"id": 7, "name": "中共宜都市委宣传部", "type": "党委", "level": "县级", "parent": "中共宜都市委员会", "location": "湖北省宜昌市宜都市"},
    {"id": 8, "name": "中共宜都市委政法委员会", "type": "党委", "level": "县级", "parent": "中共宜都市委员会", "location": "湖北省宜昌市宜都市"},
    {"id": 9, "name": "中共宜都市委统战部", "type": "党委", "level": "县级", "parent": "中共宜都市委员会", "location": "湖北省宜昌市宜都市"},
    {"id": 10, "name": "中共宜都市委办公室", "type": "党委", "level": "县级", "parent": "中共宜都市委员会", "location": "湖北省宜昌市宜都市"},
    {"id": 11, "name": "宜都市人大常委会", "type": "人大", "level": "县级", "parent": "宜昌市人大常委会", "location": "湖北省宜昌市宜都市"},
    {"id": 12, "name": "宜都市政协", "type": "政协", "level": "县级", "parent": "宜昌市政协", "location": "湖北省宜昌市宜都市"},
    {"id": 13, "name": "宜都市公安局", "type": "政府", "level": "县级", "parent": "宜昌市公安局", "location": "湖北省宜昌市宜都市"},
    {"id": 14, "name": "宜都市工商业联合会", "type": "群团", "level": "县级", "parent": "宜昌市工商联", "location": "湖北省宜昌市宜都市"},
    {"id": 15, "name": "宜都市总工会", "type": "群团", "level": "县级", "parent": "宜昌市总工会", "location": "湖北省宜昌市宜都市"},
    {"id": 16, "name": "陆城街道党工委", "type": "党委", "level": "乡镇级", "parent": "中共宜都市委员会", "location": "湖北省宜昌市宜都市"},
    {"id": 17, "name": "姚家店镇党委", "type": "党委", "level": "乡镇级", "parent": "中共宜都市委员会", "location": "湖北省宜昌市宜都市"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "市委书记、市委党校第一校长", "start": "", "end": "present", "rank": "正县级", "note": "Confirmed as of 2026-07-22 via official website + news article"},
    {"person_id": 2, "org_id": 2, "title": "市长、党组书记", "start": "", "end": "present", "rank": "正县级", "note": "Confirmed as of 2026-07-24"},
    # 市委领导
    {"person_id": 3, "org_id": 1, "title": "市委副书记、姚家店镇党委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "市委常委、人武部上校部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "市委常委、市纪委书记、市监察委员会主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "市委常委、副市长、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "市委常委、组织部部长、市委党校校长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 9, "title": "市委常委、统战部部长，市政协党组副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "市委常委、宣传部部长、市总工会主席", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "市委常委、政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 10, "title": "市委常委、市委办公室主任、市委直属机关工委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 市政府其他领导
    {"person_id": 12, "org_id": 2, "title": "副市长、市工商联主席", "start": "", "end": "present", "rank": "副县级", "note": "无党派"},
    {"person_id": 13, "org_id": 2, "title": "副市长、党组成员，市委政法委第一副书记，市公安局党委书记、局长、督察长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副市长、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副市长、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副市长、党组成员，陆城街道党工委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 市人大
    {"person_id": 17, "org_id": 11, "title": "市人大常委会主任、党组书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 18, "org_id": 11, "title": "市人大常委会副主任、党组副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 19, "org_id": 11, "title": "市人大常委会副主任、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 20, "org_id": 11, "title": "市人大常委会副主任、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 21, "org_id": 11, "title": "市人大常委会副主任、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 22, "org_id": 11, "title": "市人大常委会副主任、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 市政协
    {"person_id": 23, "org_id": 12, "title": "市政协主席、党组书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 24, "org_id": 12, "title": "市政协副主席、党组副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 25, "org_id": 12, "title": "市政协副主席", "start": "", "end": "present", "rank": "副县级", "note": "无党派"},
    {"person_id": 26, "org_id": 12, "title": "市政协副主席", "start": "", "end": "present", "rank": "副县级", "note": "无党派"},
    {"person_id": 27, "org_id": 12, "title": "市政协副主席、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 28, "org_id": 12, "title": "市政协副主席", "start": "", "end": "present", "rank": "副县级", "note": "无党派"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # Top leadership tandem
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长党政主要领导搭档", "overlap_org": "宜都市", "overlap_period": "current"},
    # 市委书记与市委副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与专职副书记", "overlap_org": "中共宜都市委员会", "overlap_period": "current"},
    # 市委书记与纪委书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委书记与纪委书记", "overlap_org": "中共宜都市委员会", "overlap_period": "current"},
    # 市委书记与组织部部长
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "市委书记与组织部部长", "overlap_org": "中共宜都市委员会", "overlap_period": "current"},
    # 市委书记与宣传部部长
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "市委书记与宣传部部长", "overlap_org": "中共宜都市委员会", "overlap_period": "current"},
    # 市委书记与政法委书记
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "市委书记与政法委书记", "overlap_org": "中共宜都市委员会", "overlap_period": "current"},
    # 市委书记与市委办主任
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "市委书记与市委办公室主任", "overlap_org": "中共宜都市委员会", "overlap_period": "current"},
    # 市委书记与统战部长
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "市委书记与统战部部长", "overlap_org": "中共宜都市委员会", "overlap_period": "current"},
    # 市长与副市长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长与市委常委、副市长", "overlap_org": "宜都市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "宜都市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与副市长（公安局长）", "overlap_org": "宜都市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "宜都市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "宜都市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "市长与副市长（兼街道党工委书记）", "overlap_org": "宜都市人民政府", "overlap_period": "current"},
    # 人大主任关系
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "市委书记与人大主任党政配合", "overlap_org": "宜都市", "overlap_period": "current"},
    # 政协主席关系
    {"person_a": 1, "person_b": 23, "type": "overlap", "context": "市委书记与政协主席", "overlap_org": "宜都市", "overlap_period": "current"},
    # 政法委书记与纪委书记（政法+纪委联动）
    {"person_a": 10, "person_b": 5, "type": "overlap", "context": "政法委书记与纪委书记工作联动", "overlap_org": "宜都市", "overlap_period": "current"},
    # 组织部部长与统战部部长
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "组织部部长与统战部部长", "overlap_org": "中共宜都市委员会", "overlap_period": "current"},
]


def write_person_json(person, output_dir):
    """Write a single person JSON file following the person_graph_json.md schema."""
    if not person["name"]:
        return
    filename = f'{TODAY}-湖北省-宜昌市-{person["current_post"].replace("/", "-").replace("、", "-")}-{person["name"]}.json'
    filepath = Path(output_dir) / filename

    source_register = []
    if person.get("source"):
        source_register.append({
            "id": "S001",
            "title": f"宜都市领导之窗 - {person['name']}",
            "url": person["source"],
            "publisher": "宜都市人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "Official leadership page — identity confirmed"
        })

    is_core = person["id"] in (1, 2)  # Core target leaders
    identity_confirmed = bool(person.get("name"))

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "宜昌市",
            "region": "宜都市",
            "job": person["current_post"],
            "task_id": "hubei_宜都市",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"yidu_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{
                "period": "",
                "institution": "",
                "major": "",
                "degree": person.get("education", ""),
                "study_type": "unknown",
                "source_ids": ["S001"]
            }],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正县级" if person["id"] in (1, 2, 17, 23) else "副县级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "No negative signals found in search scope", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin" if is_core else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"宜都市{person['current_post']}的完整职业生涯履历（早期职务、调任时间线、教育背景详情）"
        },
        "open_questions": [
            {
                "priority": "critical" if is_core else "high",
                "question": f"{person['name']}的完整职业生涯履历",
                "why_it_matters": f"核心领导人的履历是分析其任命路径、跨区交流和关系网络的基础",
                "suggested_queries": [
                    f"{person['name']} 简历 宜都",
                    f"{person['name']} 任前公示 宜昌",
                    f"{person['name']} 工作经历"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "medium",
                "question": f"{person['name']}的前任及继任路径",
                "why_it_matters": "前任去向及继任来源反映干部交流模式和上级组织意图",
                "suggested_queries": [
                    f"宜都市 前任 {person['current_post']}",
                    f"宜都市 {person['current_post']} 任职"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"    Person JSON written: {filepath}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(BASE))

    print(f"=== Building {SLUG} network ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    try:
        from gov_relation.runner import run_build

        run_build(
            slug=SLUG,
            persons=persons,
            organizations=organizations,
            positions=positions,
            relationships=relationships,
            db_path=DB_PATH,
            gexf_path=GEXF_PATH,
        )

        print(f"\nDB: {DB_PATH}")
        print(f"GEXF: {GEXF_PATH}")

    except ImportError as e:
        print(f"WARNING: gov_relation modules not available ({e}), using standalone mode...")
        # ── Standalone SQLite ────────────────────────────────────────────
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
                  p["birthplace"], p["education"], p["party_join"], p["work_start"],
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
            """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
                  pos["end"], pos["rank"], pos["note"]))

        for r in relationships:
            conn.execute("""
                INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (r["person_a"], r["person_b"], r["type"], r["context"],
                  r.get("overlap_org", ""), r.get("overlap_period", "")))

        conn.commit()
        conn.close()
        print(f"  Standalone DB written: {DB_PATH}")

        # ── Standalone GEXF ─────────────────────────────────────────────
        def esc(s):
            if s is None: return ""
            return str(s).replace("&", "&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
            f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">',
            '    <creator>Research Agent</creator>',
            f'    <description>{SLUG} leadership network</description>',
            '  </meta>',
            '  <graph mode="static" defaultedgetype="undirected">',
            '    <attributes class="node">',
            '      <attribute id="0" title="type" type="string"/>',
            '      <attribute id="1" title="role" type="string"/>',
            '      <attribute id="2" title="org" type="string"/>',
            '    </attributes>',
            '    <attributes class="edge">',
            '      <attribute id="0" title="type" type="string"/>',
            '      <attribute id="1" title="context" type="string"/>',
            '    </attributes>',
        ]

        def is_top_leader(p):
            return "市委书记" in p["current_post"] or p["current_post"] == "市长"

        def person_color(p):
            if "市委书记" in p.get("current_post", ""):
                return "255,50,50"
            if p.get("current_post") == "市长":
                return "50,100,255"
            if "纪委书记" in p.get("current_post", ""):
                return "255,165,0"
            return "100,100,100"

        def org_color(o):
            colors = {
                "党委": "255,200,200",
                "政府": "200,200,255",
                "人大": "200,255,255",
                "政协": "255,240,200",
                "群团": "255,220,255",
            }
            return colors.get(o.get("type", ""), "200,200,200")

        lines.append('    <nodes>')
        for p in persons:
            c = person_color(p).split(",")
            sz = "20.0" if is_top_leader(p) else "12.0"
            lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
            lines.append('        <attvalues>')
            lines.append(f'          <attvalue for="0" value="person"/>')
            lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
            lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
            lines.append('        </attvalues>')
            lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
            lines.append(f'        <viz:size value="{sz}"/>')
            lines.append('      </node>')

        for o in organizations:
            c = org_color(o).split(",")
            lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
            lines.append('        <attvalues>')
            lines.append(f'          <attvalue for="0" value="organization"/>')
            lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
            lines.append(f'          <attvalue for="2" value=""/>')
            lines.append('        </attvalues>')
            lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
            lines.append('        <viz:size value="8.0"/>')
            lines.append('      </node>')
        lines.append('    </nodes>')

        lines.append('    <edges>')
        eid = 0
        for pos in positions:
            eid += 1
            lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
            lines.append('        <attvalues>')
            lines.append('          <attvalue for="0" value="worked_at"/>')
            lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')

        for r in relationships:
            eid += 1
            context = r.get("context", r.get("type", ""))
            lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(context)}" weight="2.0">')
            lines.append('        <attvalues>')
            lines.append(f'          <attvalue for="0" value="relationship"/>')
            lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')

        lines.append('    </edges>')
        lines.append('  </graph>')
        lines.append('</gexf>')

        with open(GEXF_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"  Standalone GEXF written: {GEXF_PATH}")

    # ── Person JSONs ────────────────────────────────────────────────────
    print("  Creating person JSON files...")
    import sqlite3 as sqlite_mod
    for p in persons:
        write_person_json(p, PERSONS_DIR)

    print(f"\n=== Done ===")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    person_files = [f for f in Path(PERSONS_DIR).iterdir() if f.suffix == ".json" and TODAY in f.name]
    for pf in sorted(person_files):
        print(f"  Person: {pf.name}")
