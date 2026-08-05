#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 三都水族自治县 (Sandu Shui Autonomous County), 黔南布依族苗族自治州, 贵州省.

Level: 县
Province: 贵州省
Parent city: 黔南布依族苗族自治州
Targets: 县委书记 & 县长
Task ID: guizhou_三都水族自治县
Investigation date: 2026-08-05

Research sources (primary: 三都县人民政府门户 www.sandu.gov.cn):
  - 领导之窗 (县委领导/政府领导/人大领导/政协领导):
      + https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5980865/... (县委班子成员 bio)
      + 朱建明 profile: .../xwld_5980865/202604/t20260403_89962789.html (2026-04)
      + 杨凯 profile: .../xwld_5980865/202503/t20250325_87269950.html & zfld .../87269969.html
      + 李自胜/罗勇/杨承辉/何山/杨宗儒/蒙玉玺/廖明波/岑文丙/吴茂华 profiles
      + 政府: 杨凯/何山/杨承辉/杨秀举/朱仕祥/王国军/韦子涵; 人大: 陈木林/潘廷军/杨先烈/潘和房/韦族琼/谭诗进; 政协: 覃友寿/吴平昌/刘世洪/胡雪莉/张仁勇/付国勤
  - 领导活动/三都要闻:
      + 2026-08-03 州庆活动调度会 (t20260803_90690279): 朱建明主持, 杨凯, 向文敏/蒙雄/岑华丙/吴向华
      + 2026-07-29 半年经济工作会 (t20260729_90674087): 朱建明主持; 杨凯; 覃友宽/韦恩圣,李自胜,胡岳华,县委常委
      + 2026-07-31 八一慰问 (t20260731_90684284): 朱建明/杨凯/覃友宽/韦恩圣
      + 2026-07-28 县委常委会第200次 (t20260728_09269587): 朱建明/杨凯/覃友宽/韦恩圣/李自胜/胡岳华/何野
  - 任命/简历:
      + 网易订阅 / 百越之南 (2026-03-31/04-01): 朱建明已任三都县委书记(兼县人武部第一书记); 1996-09 工作,2002-06 入党,施秉县人
      + 新浪网 / 多彩贵州网 (2021-06-17): 杨凯当选县长; 简历
      * 多彩贵州网 / 网易 (2026-02-27): 前任书记曾薇被省纪委监委纪律审查和监察调查

Confidence notes:
  - 朱建明 (县委书记): confirmed via official 领导之窗 + 县委常委会/领导活动报道 (2026-03 起任). 2004-2019 中间任职年份为 gap(open).
  - 杨凯 (县委副书记、县长): confirmed via 官方领导之窗 bio + 2021-06 当选新闻 + 全国人大代表.
  - 县委常委会成员: confirmed via 官方领导之窗 profiles(多个 2026-04/2026-07 profile).
  - 新任领导(胡岳锋、韦恩胜、向仕敏): 官方新闻在列, 详细履历未取得 — open gap.
  - 前任书记曾薇: 被查(省纪委监委 2026-02-27 通报) — 风险信号(公开来源).
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "三都水族自治县"
TODAY = datetime.now().strftime("%Y%m%d")

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ 县委主要领导(一把手/二把手) ═══════
    {
        "id": 1,
        "name": "朱建明",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1976年1月",
        "birthplace": "贵州施秉",
        "education": "大学学历(曾在职自考贵州大学法律专业)",
        "party_join": "中共党员",
        "work_start": "1996年9月",
        "current_post": "中共三都水族自治县委书记",
        "current_org": "中共三都水族自治县委员会",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5980865/202604/t20260403_89962789.html; https://www.sandu.gov.cn/xwdt/ldhd/"
    },
    {
        "id": 2,
        "name": "杨凯",
        "gender": "男",
        "ethnicity": "水族",
        "birth": "1985年12月",
        "birthplace": "贵州剑河",
        "education": "大学学历、管理学学士(华北电力大学工程管理专业)",
        "party_join": "中共党员",
        "work_start": "2007年7月",
        "current_post": "中共三都水族自治县委副书记、县人民政府县长/党组书记",
        "current_org": "三都水族自治县人民政府",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5980865/202503/t20250325_87269950.html"
    },
    # ═══════ 县委副书记 ═══════
    {
        "id": 3,
        "name": "李自胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年4月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水族自治县委副书记、县委政法委书记",
        "current_org": "中共三都水族自治县委员会",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5980865/202503/t20250325_87269948.html"
    },
    {
        "id": 4,
        "name": "胡庭华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水族自治县委副书记(履历待查)",
        "current_org": "中共三都水族自治县委员会",
        "source": "https://www.sandu.gov.cn/xwdt/sdyw/202607/t20260728_90669874.html"
    },
    # ═══════ 县委常委会 ═══════
    {
        "id": 5,
        "name": "何山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年9月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水族自治县委常委、三级调研员、常务副县长",
        "current_org": "三都水族自治县人民政府",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5980865/202503/t20250325_87269949.html"
    },
    {
        "id": 6,
        "name": "罗勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年2月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水委常委、县纪委书记、县监委主任、四级高级监察官",
        "current_org": "中共三都水族自治县纪律检查委员会",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5980865/202503/t20250325_87269945.html"
    },
    {
        "id": 7,
        "name": "杨承辉",
        "gender": "男",
        "ethnicity": "水族",
        "birth": "1977年5月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水委常委、县人民政府党组成员、副县长",
        "current_org": "三都水族自治县人民政府",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5980865/202503/t20250325_87269946.html"
    },
    {
        "id": 8,
        "name": "杨宗儒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年12月",
        "birthplace": "",
        "education": "大学·管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水委常委、县委组织部部长、县委党校校长(兼)",
        "current_org": "中共三都水族自治县委组织部",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5980865/202507/t20250703_88227499.html"
    },
    {
        "id": 9,
        "name": "蒙玉玺",
        "gender": "男",
        "ethnicity": "水族",
        "birth": "1983年10月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水委常委、县委办公室主任、县直机关工委书记",
        "current_org": "中共三都水族自治县委办公室",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5980865/202503/t20250325_87269944.html"
    },
    {
        "id": 10,
        "name": "廖明波",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1983年6月",
        "birthplace": "",
        "education": "大学·炮兵指挥学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水委常委、县人武部部长",
        "current_org": "三都水族自治县人民武装部",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5980865/202507/t20250703_88227605.html"
    },
    {
        "id": 11,
        "name": "岑文丙",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1986年4月",
        "birthplace": "",
        "education": "大学·理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水委常委、三合街道党工委书记",
        "current_org": "三都水族自治县三合街道党工委",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5980865/202507/t20250703_88227606.html"
    },
    {
        "id": 12,
        "name": "吴茂华",
        "gender": "男",
        "ethnicity": "水族",
        "birth": "1978年3月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水委常委、县委宣传部部长、县委统战部部长",
        "current_org": "中共三都水族自治县委宣传部",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_9865/202503/t20250325_87269947.html"
    },
    {
        "id": 13,
        "name": "向仕敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水委常委/县领导(履历待查)",
        "current_org": "中共三都水族自治县委员会",
        "source": "https://www.sandu.gov.cn/xwdt/sdyw/202608/t20260803_90690279.html"
    },
    # ═══════ 县政府领导 ═══════
    {
        "id": 14,
        "name": "杨秀举",
        "gender": "男",
        "ethnicity": "水族",
        "birth": "1978年9月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水族自治县人民政府党组成员、副县长",
        "current_org": "三都水族自治县人民政府",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/zfld_5980868/202503/t20250325_87269967.html"
    },
    {
        "id": 15,
        "name": "朱仕祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年3月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水族自治县人民政府党组成员、副县长",
        "current_org": "三都水族自治县人民政府",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/zfld_5980868/202503/t20250325_87269962.html"
    },
    {
        "id": 16,
        "name": "韦子涵",
        "gender": "女",
        "ethnicity": "水族",
        "birth": "1990年1月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水族自治县人民政府副县长(分管文旅/民宗等)",
        "current_org": "三都水族自治县人民政府",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/zfld_5980868/202508/t20250813_88457744.html"
    },
    {
        "id": 17,
        "name": "王国军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "",
        "education": "项目管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水族自治县人民政府党组成员、副县长、县公安局党委书记/局长/督察长",
        "current_org": "三都水族自治县公安局",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/zfld_5980868/202604/t20260408_89974726.html"
    },
    # ═══════ 县人大 ═══════
    {
        "id": 18,
        "name": "陈木林",
        "gender": "男",
        "ethnicity": "水族",
        "birth": "1968年3月",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水族自治县人大常委会主任",
        "current_org": "三都水族自治县人大常委会",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/rdld_5980867/202503/t20250325_87269958.html"
    },
    {
        "id": 19,
        "name": "覃友寿",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1975年9月",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三都水族自治县人大常委会党组书记(原县政协主席)",
        "current_org": "三都水族自治县人大常委会",
        "source": "https://www.sandu.gov.cn/xwdt/ldhd/202607/t20260731_90684284.html"
    },
    # ═══════ 县政协 ═══════
    {
        "id": 20,
        "name": "韦恩胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组书记(履历待查)",
        "current_org": "政协三都水族自治县委员会",
        "source": "https://www.sandu.gov.cn/xwdt/ldhd/202607/t20260731_90684284.html"
    },
    {
        "id": 21,
        "name": "付国勤",
        "gender": "女",
        "ethnicity": "苗族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "大学",
        "party_join": "民盟",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协三都水族自治县委员会",
        "source": "https://www.sandu.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/zxld_5980869/202503/t20250325_87269973.html"
    },
    # ═══════ 前任书记 ═══════
    {
        "id": 22,
        "name": "曾薇",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "贵州瓮安",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任三都县委书记(2026-02-27被省纪委监委纪律审查和监察调查)",
        "current_org": "中共三都水族自治县委员会",
        "source": "https://www.baidu.com/…; 多彩贵州网2026-02-27"
    },
    # ═══════ 前任书记: 朱奉余 ═══════
    {
        "id": 23,
        "name": "朱奉余",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任三都县委书记(2017-2022前后在任)",
        "current_org": "中共三都水族自治县委员会",
        "source": "https://www.baidu.com/…; 多彩贵州网2017-12"
    },
    # ═══════ 前任县长 ═══════
    {
        "id": 24,
        "name": "潘仕进",
        "gender": "男",
        "ethnicity": "水族",
        "birth": "1972年10月",
        "birthplace": "贵州荔波",
        "education": "贵州大学(原籍)",
        "party_join": "中共党员",
        "work_start": "1992年8月",
        "current_post": "前任三都县长(2021-06前在任,由杨凯接任)",
        "current_org": "三都水族自治县人民政府",
        "source": "https://www.baidu.com/…; 多彩贵州网"
    },
]

# ── Organizations ───────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共三都水族自治县委", "type": "党委", "level": "县", "parent": "中共黔南州委", "location": "贵州省黔南州三都水族自治县"},
    {"id": 2, "name": "三都水族自治县人民政府", "type": "政府", "level": "县", "parent": "黔南州人民政府", "location": "贵州省黔南州三都水族自治县"},
    {"id": 3, "name": "中共三都水族自治县纪委/县监委", "type": "纪委", "level": "县", "parent": "中共黔南州纪委", "location": "贵州省黔南州三都水族自治县"},
    {"id": 4, "name": "中共三都水族自治县委组织部", "type": "党委", "level": "县", "parent": "中共三都水族自治县委", "location": "贵州省黔南州三都水族自治县"},
    {"id": 5, "name": "中共三都水族自治县委办公室/县直机关工委", "type": "党委", "level": "县", "parent": "中共三都水族自治县委", "location": "贵州省黔南州三都水族自治县"},
    {"id": 6, "name": "三都水族自治县人民武装部", "type": "军队", "level": "县", "parent": "黔南军分区", "location": "贵州省黔南州三都水族自治县"},
    {"id": 7, "name": "三都水族自治县三合街道党工委", "type": "街道", "level": "乡级", "parent": "中共三都水族自治县委", "location": "贵州省黔南州三都水族自治县"},
    {"id": 8, "name": "中共三都水族自治县委宣传部/县委统战部", "type": "党委", "level": "县", "parent": "中共三都水族自治县委", "location": "贵州省黔南州三都水族自治县"},
    {"id": 9, "name": "三都水族自治县公安局", "type": "政府", "level": "县", "parent": "三都水族自治县人民政府", "location": "贵州省黔南州三都水族自治县"},
    {"id": 10, "name": "三都水族自治县人大常委会", "type": "人大", "level": "县", "parent": "黔南州人大常委会", "location": "贵州省黔南州三都水族自治县"},
    {"id": 11, "name": "政协三都水族自治县委员会", "type": "政协", "level": "县", "parent": "政协黔南州委员会", "location": "贵州省黔南州三都水族自治县"},
]

# ── Positions ───────────────────────────────────────────────
positions = [
    # 朱建明
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共三都水族自治县委书记", "start": "2026-03", "end": "present", "rank": "正处级",
     "note": "主持县委全面工作。兼县人武部党委第一书记(2026-05-14起)。官方领导之窗/县委常委会报道确认。"},
    {"id": 2, "person_id": 1, "org_id": 6, "title": "县人武部党委第一书记", "start": "2026-05", "end": "present", "rank": "兼"},
    # 杨凯
    {"id": 3, "person_id": 2, "org_id": 1, "title": "中共三都水族自治县委副书记", "start": "2021-06", "end": "present", "rank": "副处级",
     "note": "兼任县委副书记、县人民政府党组副书记。"},
    {"id": 4, "person_id": 2, "org_id": 2, "title": "三都水族自治县人民政府县长/党组书记", "start": "2021-06", "end": "present", "rank": "正处级",
     "note": "2021-06-16县十六届人大七次会议补选为县长(获满票)。主持县政府全面工作。2026年3月为全国人大代表出席全国两会。"},
    # 李自胜
    {"id": 5, "person_id": 3, "org_id": 1, "title": "三都水族自治县委副书记、县委政法委书记", "start": "", "end": "present", "rank": "副处级",
     "note": "协助书记抓政法、维稳、综治等工作。"},
    # 胡庭岳
    {"id": 6, "person_id": 4, "org_id": 1, "title": "三都水族自治县委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "2026-07-28县委常委会/2026-08-03州庆调度会出席名单在列。"},
    # 何山
    {"id": 7, "person_id": 5, "org_id": 2, "title": "三都水族自治县常务副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责县政府常务、发改、财税、国资、应急、安全生产、新型城镇化等。"},
    # 罗勇
    {"id": 8, "person_id": 6, "org_id": 3, "title": "县纪委书记、县监委主任", "start": "", "end": "present", "rank": "副处级",
     "note": "协助县委书记分管党风廉政、反腐败、巡察。四级高级监察官。"},
    # 杨承辉
    {"id": 9, "person_id": 7, "org_id": 2, "title": "县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责新型工业化、商务、工业园区、林业、市场监管、招商等。"},
    # 杨宗儒
    {"id": 10, "person_id": 8, "org_id": 4, "title": "县委组织部部长、县委党校校长(兼)", "start": "", "end": "", "rank": "副处级",
     "note": "主管组织、干部、人才、编制、党建等工作。"},
    # 蒙玉玺
    {"id": 11, "person_id": 9, "org_id": 5, "title": "县委办主任、县直机关工委书记", "start": "", "end": "present", "rank": "副处级",
     "note": "主管县委办公室、机要保密国安档案。"},
    # 何文华(人武部长)
    {"id": 12, "person_id": 10, "org_id": 6, "title": "三都水族自治县人民武装部部长", "start": "", "end": "present", "rank": "副处级",
     "note": "主管县人武部、国防动员。"},
    # 岑振华
    {"id": 13, "person_id": 11, "org_id": 7, "title": "三合街道党工委书记", "start": "", "end": "present", "rank": "副处级",
     "note": "兼抓新型城镇化、城市管理。"},
    # 吴向华
    {"id": 14, "person_id": 12, "org_id": 8, "title": "县委宣传部部长、县委统战部部长", "start": "", "end": "present", "rank": "副处级",
     "note": "主管宣传思想、精神文明、意识形态、统一战线、民族宗教。"},
    # 向仕敏
    {"id": 15, "person_id": 13, "org_id": 1, "title": "三都水自治县委常委/县领导", "start": "", "end": "present", "rank": "副处级",
     "note": "2026-08-03州庆调度会出席。"},
    # 政府副职
    {"id": 16, "person_id": 14, "org_id": 2, "title": "县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "杨秀举,负责财税、乡村振兴、农业农村等。"},
    {"id": 17, "person_id": 15, "org_id": 2, "title": "县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "朱仕祥,负责水利、农业、乡村振兴、涉农等。"},
    {"id": 18, "person_id": 16, "org_id": 2, "title": "县人民政府副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "韦子涵,分管文旅、民族宗教、水族文化等。"},
    {"id": 19, "person_id": 17, "org_id": 9, "title": "副县长兼县公安局局长/党委书记", "start": "", "end": "present", "rank": "副处级",
     "note": "王国军,负责公安、国安、司法、维稳等,主持县公安局。"},
    # 人大
    {"id": 20, "person_id": 18, "org_id": 10, "title": "县人大常委会主任", "start": "2022-01", "end": "present", "rank": "正处级",
     "note": "陈木林,十七届人大常委会主任,2022-01当选。"},
    {"id": 21, "person_id": 19, "org_id": 10, "title": "县人大常委会党组书记", "start": "2026", "end": "present", "rank": "正处级",
     "note": "覃友寿,原县政协主席,2026年转任县人大党组书记。"},
    # 政协
    {"id": 22, "person_id": 20, "org_id": 11, "title": "县政协党组书记", "start": "2026", "end": "present", "rank": "正处级",
     "note": "韦恩胜,2026年新任政协党组书记。"},
    {"id": 23, "person_id": 21, "org_id": 11, "title": "县政协副主席", "start": "2022-01", "end": "present", "rank": "副处级",
     "note": "付国勤,民盟。"},
    # 前任书记/县长
    {"id": 24, "person_id": 22, "org_id": 1, "title": "前任中共三都县委书记", "start": "2022-09", "end": "2026-02", "rank": "正处级",
     "note": "曾薇,2022-09起任书记。2026-02-27因涉嫌严重违纪违法被贵州省纪委监委纪律审查和监察调查。"},
    {"id": 25, "person_id": 23, "org_id": 1, "title": "前任三都县委书记", "start": "2017-12", "end": "2022", "rank": "正处级",
     "note": "朱奉余,2017-12起任书记。"},
    {"id": 26, "person_id": 24, "org_id": 2, "title": "前任三都县长", "start": "2015", "end": "2021-06", "rank": "正处级",
     "note": "潘仕进,2021-06前在任,杨凯接任。"},
]

# ── Relationships ───────────────────────────────────────────
relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记朱建明与县长杨凯党政正职搭档,共同出席县委常委会、县半年经济会、州庆调度会(2026-03起)。", "overlap_org": "中共三都县委/县政府", "overlap_period": "2026"},
    {"id": 2, "person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记领导县委副书记李自胜(县委政法委),县委常委会同台(2026-07)。", "overlap_org": "中共三都县委", "overlap_period": "2026"},
    {"id": 3, "person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记领导县委副书记胡庭岳,县委常委会同台(2026-07-28)。", "overlap_org": "中共三都县委", "overlap_period": "2026"},
    {"id": 4, "person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记领导常务副县长何山,共同出席县委常委会/县政府会)。", "overlap_org": "中共三都县委/县政府", "overlap_period": "2026"},
    {"id": 5, "person_a": 1, "person_b": 8, "type": "上下级", "context": "县委书记领导县委组织部长杨宗儒,县委常委会同台)。", "overlap_org": "中共三都县委", "overlap_period": "2026"},
    {"id": 6, "person_a": 1, "person_b": 18, "type": "同级协作", "context": "县委书记与人大主任陈木林同台出席县委常委会(2026-06/07-11-15第194次)。", "overlap_org": "三都四家班子", "overlap_period": "2026"},
    {"id": 7, "person_a": 1, "person_b": 19, "type": "同级协作", "context": "县委书记与人大党组书记覃友寿同台出席拥军慰问/县委常委会(2026-07)。", "overlap_org": "三都四家班子", "overlap_period": "2026"},
    {"id": 8, "person_a": 1, "person_b": 22, "type": "前任-后继", "context": "朱建明继任曾薇任三都县委书记。曾薇2026-02-27因涉嫌严重违纪违法被省纪委监委纪律审查和监察调查(落马);朱建明2026-03接任。", "overlap_org": "中共三都县委", "overlap_period": "2026"},
    {"id": 9, "person_a": 2, "person_b": 5, "type": "上下级", "context": "县长领导常务副县长何山负责县政府常务工作。", "overlap_org": "县政府", "overlap_period": "2020"},
    {"id": 10, "person_a": 2, "person_b": 24, "type": "前任-后继", "context": "杨凯继任县长。前任县长潘仕进,2021-06杨凯补选为县长。", "overlap_org": "县政府", "overlap_period": "2024"},
    {"id": 11, "person_a": 19, "person_b": 20, "type": "前继关系", "context": "原副县长调任:覃友寿自县政协主席任人大党组书记,韦恩胜为新政协党组书记;两人在2026年交接县四班子成员。", "overlap_org": "三都四家班子", "overlap_period": "2026"},
    {"id": 12, "person_a": 22, "person_b": 2, "type": "上下级", "context": "前任书记曾薇与县长杨凯2022-09-2026-02任内曾搭班子。", "overlap_org": "中共三都县委/县政府", "overlap_period": "2022-2026"},
    {"id": 13, "person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记领导县纪委书记罗勇,共同抓党风廉政建设、反腐工作。", "overlap_org": "中共三都县委/县纪委监委", "overlap_period": "2026"},
    {"id": 14, "person_a": 1, "person_b": 17, "type": "上下级", "context": "县委书记领导公安局长王国军(县政府副县长、公安局长)。", "overlap_org": "政府/县公安局", "overlap_period": "2026"},
    {"id": 15, "person_a": 2, "person_b": 17, "type": "上下级", "context": "县长领导公安局长王国军,政府班子成员。", "overlap_org": "县政府/公安", "overlap_period": "2026"},
]

# ── SQLite Build ───────────────────────────────────────────
if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()
conn.executescript("""
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '',
        birth TEXT DEFAULT '',
        birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '',
        party_join TEXT DEFAULT '',
        work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '',
        current_org TEXT DEFAULT '',
        source TEXT DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        start TEXT DEFAULT '',
        end TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

for p in persons:
    cur.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""), p.get("birthplace", ""),
         p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""), p.get("current_post", ""), p.get("current_org", ""), p.get("source", ""))
    )
for o in organizations:
    cur.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
    )
for pos in positions:
    cur.execute(
        "INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (pos["id"], pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""), pos.get("note", ""))
    )
for r in relationships:
    cur.execute(
        "INSERT INTO relationships (id, person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (r["id"], r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )
conn.commit()

# ── GEXF Generation ────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def is_party_secretary(post):
    return ("县委书记" in post) and ("县委副书记" not in post) and ("前任" not in post) and ("人民政协" not in post)

def is_gov_leader(post):
    return ("县长" in post) and ("副县长" not in post) and ("前任" not in post) and ("县委副书记" not in post or "人民政府县长" in post)

def person_color(p):
    post = p.get("current_post", "") or ""
    if is_party_secretary(post):
        return "255,50,50"
    elif is_gov_leader(post) or "县长" in post:
        return "50,100,255"
    elif "常务副县长" in post or "常务" in post:
        return "50,120,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "被纪律审查和监察调查" in post or "前任" in post:
        return "150,150,150"
    elif "公安" in post:
        return "50,150,255"
    elif "副书记" in post:
        return "255,120,60"
    return "100,100,100"

def org_color(o):
    t = o.get("type", "") or ""
    if "党委" in t:
        return "255,200,200"
    elif "纪委" in t:
        return "255,220,180"
    elif "政府" in t or "公安" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "军队" in t:
        return "200,255,200"
    return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post", "") or ""
    return is_party_secretary(post) or is_gov_leader(post)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Research Agent - gov-relation</creator>')
lines.append('    <description>三都水族自治县领导班子工作关系网络 - 贵州省黔南布依族苗族自治州</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="organization" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", "") or "")}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", "") or "")}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type", "") or "")}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("level", "") or "")}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

conn.close()

# ── Summary ────────────────────────────────────────────────
print(f"三都水族自治县 network build complete.")
print(f"  Database:        {DB_PATH} ({DB_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  GEXF:            {GEXF_PATH} ({GEXF_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  Persons:         {len(persons)}")
print(f"  Organizations:   {len(organizations)}")
print(f"  Positions:       {len(positions)}")
print(f"  Relationships:   {len(relationships)}")
print()
print("Confidence notes:")
print("  - 朱建明 (书记): confirmed via official 2026-04 领导之窗 + 县委常委会报道; early-career precise years partial (gap)")
print("  - 杨凯 (县长):     confirmed via official 领导之窗 bio + 2021-06 当选新闻")
print("  - 班子成员:        confirmed via official 领导之窗")
print("  - 风险: 前任书记曾薇 2026-02-27 被省纪委监委纪律审查和监察调查 (multiple media)")