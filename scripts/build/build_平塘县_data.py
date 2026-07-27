#!/usr/bin/env python3
"""Build script for 平塘县 (Pingtang County, Qiannan, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县
Province: 贵州省
Parent City: 黔南布依族苗族自治州
Targets: 县委书记 & 县长

Research Note:
  All data sourced directly from 平塘县人民政府官方网站 (www.gzpt.gov.cn) - 领导之窗
  page, which lists the full leadership team with name, ethnicity, birth date,
  education, and brief biographies. No individual career timeline beyond the
  current role was available on the government site. Predecessor information
  was not found on the accessible pages.

  Web search (Exa, Baidu, Google) was rate-limited or blocked. 百度百科 was
  inaccessible (403). All research was completed via direct HTTP access to the
  government website at http://www.gzpt.gov.cn/.

Sources:
  - http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (leadership page index)
  - http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202602/t20260214_89557142.html (石磊)
  - http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/zfld/202602/t20260214_89557116.html (莫艳)
  - http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202503/t20250328_87293200.html (蒙祖伟)
  - http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202503/t20250328_87293199.html (孙亚吉)
  - http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202503/t20250328_87293191.html (赵中策)
  - http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202602/t20260228_89589977.html (徐亚梓)
  - http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202503/t20250328_87293188.html (陈以惠)
  - http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202511/t20251113_88939970.html (王波)
  - http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202602/t20260228_89589771.html (邓庆梅)
  - http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202605/t20260515_90177203.html (刘旭阳)
"""

import sqlite3  # noqa: used by gov_relation.runner
from pathlib import Path

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    # 1. 县委书记 (Party Secretary)
    {
        "id": 1,
        "name": "石磊",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1982年9月",
        "birthplace": "",
        "education": "大学本科，文学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "平塘县委书记",
        "current_org": "中共平塘县委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202602/t20260214_89557142.html",
    },
    # 2. 县长 (County Mayor)
    {
        "id": 2,
        "name": "莫艳",
        "gender": "女",
        "ethnicity": "布依族",
        "birth": "1979年8月",
        "birthplace": "",
        "education": "大学本科，法学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "平塘县委副书记、县长，县政府党组书记",
        "current_org": "平塘县人民政府",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/zfld/202602/t20260214_89557116.html",
    },
    # ── 县委常委 (Party Standing Committee) ──
    # 3. 常务副县长
    {
        "id": 3,
        "name": "蒙祖伟",
        "gender": "男",
        "ethnicity": "水族",
        "birth": "1979年7月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县人民政府常务副县长",
        "current_org": "平塘县人民政府",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202503/t20250328_87293200.html",
    },
    # 4. 组织部长
    {
        "id": 4,
        "name": "孙亚吉",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1984年5月",
        "birthplace": "",
        "education": "贵州大学，本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县委组织部部长、县委党校校长（兼）",
        "current_org": "中共平塘县委组织部",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202503/t20250328_87293199.html",
    },
    # 5. 县委办主任
    {
        "id": 5,
        "name": "赵中策",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县委办主任、县直属机关工委书记、县委国安办主任",
        "current_org": "中共平塘县委办公室",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202503/t20250328_87293191.html",
    },
    # 6. 纪委书记
    {
        "id": 6,
        "name": "徐亚梓",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1981年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共平塘县纪律检查委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202602/t20260228_89589977.html",
    },
    # 7. 金盆街道书记 (县委常委)
    {
        "id": 7,
        "name": "陈以惠",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1976年1月",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、金盆街道党工委书记",
        "current_org": "中共平塘县金盆街道工作委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202503/t20250328_87293188.html",
    },
    # 8. 副县长（县委常委）
    {
        "id": 8,
        "name": "王波",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1978年6月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县人民政府副县长",
        "current_org": "平塘县人民政府",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202511/t20251113_88939970.html",
    },
    # 9. 宣传/统战部长
    {
        "id": 9,
        "name": "邓庆梅",
        "gender": "女",
        "ethnicity": "水族",
        "birth": "1986年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县委宣传部部长、县委统战部部长",
        "current_org": "中共平塘县委宣传部",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202602/t20260228_89589771.html",
    },
    # 10. 人武部长
    {
        "id": 10,
        "name": "刘旭阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、人武部上校部长",
        "current_org": "平塘县人民武装部",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202605/t20260515_90177203.html",
    },
    # 11. 挂职副县长
    {
        "id": 11,
        "name": "黎伟谦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县人民政府副县长（挂职）",
        "current_org": "平塘县人民政府",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202512/t20251226_89093884.html",
    },
    # 12. 挂职副县长
    {
        "id": 12,
        "name": "黄焱",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委，县人民政府党组成员、副县长（挂职）",
        "current_org": "平塘县人民政府",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/xwld_5982014/202512/t20251226_89093817.html",
    },
    # ── 县政府其他领导 (Other Government Leaders) ──
    # 13.
    {
        "id": 13,
        "name": "杨俊程",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "平塘县人民政府",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗政府领导列表)",
    },
    # 14.
    {
        "id": 14,
        "name": "雷贵桃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "平塘县人民政府",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗政府领导列表)",
    },
    # 15.
    {
        "id": 15,
        "name": "王朝虎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平塘县人民政府副县长",
        "current_org": "平塘县人民政府",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗政府领导列表)",
    },
    # 16.
    {
        "id": 16,
        "name": "鲍恩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平塘县人民政府副县长",
        "current_org": "平塘县人民政府",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗政府领导列表)",
    },
    # ── 县人大 (People's Congress) ──
    # 17.
    {
        "id": 17,
        "name": "韦永忠",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1978年4月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "平塘县人民代表大会常务委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗人大领导列表)",
    },
    # 18.
    {
        "id": 18,
        "name": "曾昭洪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会党组副书记、副主任",
        "current_org": "平塘县人民代表大会常务委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗人大领导列表)",
    },
    # 19.
    {
        "id": 19,
        "name": "吴家福",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "平塘县人民代表大会常务委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗人大领导列表)",
    },
    # 20.
    {
        "id": 20,
        "name": "杨本环",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "平塘县人民代表大会常务委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗人大领导列表)",
    },
    # 21.
    {
        "id": 21,
        "name": "陆光明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "平塘县人民代表大会常务委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗人大领导列表)",
    },
    # 22.
    {
        "id": 22,
        "name": "戴德",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会党组成员、副主任、县财政局党组书记",
        "current_org": "平塘县人民代表大会常务委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗人大领导列表)",
    },
    # 23.
    {
        "id": 23,
        "name": "刘凤桃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "平塘县人民代表大会常务委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗人大领导列表)",
    },
    # ── 县政协 (CPPCC) ──
    # 24.
    {
        "id": 24,
        "name": "莫卫武",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1966年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席、党组书记",
        "current_org": "中国人民政治协商会议平塘县委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗政协领导列表)",
    },
    # 25.
    {
        "id": 25,
        "name": "田仁飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席、党组成员",
        "current_org": "中国人民政治协商会议平塘县委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗政协领导列表)",
    },
    # 26.
    {
        "id": 26,
        "name": "王国敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席、党组成员",
        "current_org": "中国人民政治协商会议平塘县委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗政协领导列表)",
    },
    # 27.
    {
        "id": 27,
        "name": "刘忠燕",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议平塘县委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗政协领导列表)",
    },
    # 28.
    {
        "id": 28,
        "name": "彭皓",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协党组成员",
        "current_org": "中国人民政治协商会议平塘县委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗政协领导列表)",
    },
    # 29.
    {
        "id": 29,
        "name": "罗敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席、党组成员",
        "current_org": "中国人民政治协商会议平塘县委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗政协领导列表)",
    },
    # 30.
    {
        "id": 30,
        "name": "陈国本",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席、党组成员",
        "current_org": "中国人民政治协商会议平塘县委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗政协领导列表)",
    },
    # 31.
    {
        "id": 31,
        "name": "文庆超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席、党组成员",
        "current_org": "中国人民政治协商会议平塘县委员会",
        "source": "http://www.gzpt.gov.cn/zwgk_500411/zfxxgkml/jcxxgk/ldzc/ (领导之窗政协领导列表)",
    },
]

ORGANIZATIONS = [
    # ── 党委 (Party) ──
    {"id": 1, "name": "中共平塘县委员会", "type": "党委", "level": "县", "location": "平塘县"},
    {"id": 2, "name": "中共平塘县委组织部", "type": "党委", "level": "县", "location": "平塘县"},
    {"id": 3, "name": "中共平塘县委办公室", "type": "党委", "level": "县", "location": "平塘县"},
    {"id": 4, "name": "中共平塘县纪律检查委员会", "type": "党委", "level": "县", "location": "平塘县"},
    {"id": 5, "name": "中共平塘县委宣传部", "type": "党委", "level": "县", "location": "平塘县"},
    {"id": 6, "name": "中共平塘县金盆街道工作委员会", "type": "党委", "level": "街道", "location": "平塘县金盆街道"},
    # ── 政府 (Government) ──
    {"id": 7, "name": "平塘县人民政府", "type": "政府", "level": "县", "location": "平塘县"},
    # ── 人大 (People's Congress) ──
    {"id": 8, "name": "平塘县人民代表大会常务委员会", "type": "人大", "level": "县", "location": "平塘县"},
    # ── 政协 (CPPCC) ──
    {"id": 9, "name": "中国人民政治协商会议平塘县委员会", "type": "政协", "level": "县", "location": "平塘县"},
    # ── 军事 (Military) ──
    {"id": 10, "name": "平塘县人民武装部", "type": "事业单位", "level": "县", "location": "平塘县"},
    # ── 乡镇/街道 ──
    {"id": 11, "name": "平塘县金盆街道办事处", "type": "乡镇/街道", "level": "街道", "location": "平塘县金盆街道"},
]

POSITIONS = [
    # 石磊
    {"person_id": 1, "org_id": 1, "title": "平塘县委书记", "start": "", "end": "present", "rank": "正县级", "note": "主持县委全面工作"},
    # 莫艳
    {"person_id": 2, "org_id": 1, "title": "平塘县委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "县长，县政府党组书记", "start": "", "end": "present", "rank": "正县级", "note": "领导县政府全面工作"},
    # 蒙祖伟
    {"person_id": 3, "org_id": 7, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "副县级", "note": "协助抓经济、审计、财经"},
    # 孙亚吉
    {"person_id": 4, "org_id": 2, "title": "县委常委、组织部部长、县委党校校长（兼）", "start": "", "end": "present", "rank": "副县级", "note": "主持组织部工作"},
    # 赵中策
    {"person_id": 5, "org_id": 3, "title": "县委常委、县委办主任、县直属机关工委书记、县委国安办主任", "start": "", "end": "present", "rank": "副县级", "note": "主持县委办工作"},
    # 徐亚梓
    {"person_id": 6, "org_id": 4, "title": "县委常委、县纪委书记、县监委主任", "start": "", "end": "present", "rank": "副县级", "note": "负责纪委全面工作"},
    # 陈以惠
    {"person_id": 7, "org_id": 6, "title": "县委常委、金盆街道党工委书记", "start": "", "end": "present", "rank": "副县级", "note": "主持金盆街道全面工作"},
    # 王波
    {"person_id": 8, "org_id": 7, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责自然资源、住建、环保等"},
    # 邓庆梅
    {"person_id": 9, "org_id": 5, "title": "县委常委、宣传部部长、统战部部长", "start": "", "end": "present", "rank": "副县级", "note": "主持宣传部、统战部工作"},
    # 刘旭阳
    {"person_id": 10, "org_id": 10, "title": "县委常委、人武部上校部长", "start": "", "end": "present", "rank": "副县级", "note": "主持县人武部工作"},
    # 黎伟谦
    {"person_id": 11, "org_id": 7, "title": "县委常委、副县长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "挂职"},
    # 黄焱
    {"person_id": 12, "org_id": 7, "title": "县委常委、副县长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "挂职"},
    # 杨俊程
    {"person_id": 13, "org_id": 7, "title": "县政府党组成员、副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 雷贵桃
    {"person_id": 14, "org_id": 7, "title": "县政府党组成员、副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 王朝虎
    {"person_id": 15, "org_id": 7, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 鲍恩
    {"person_id": 16, "org_id": 7, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 韦永忠
    {"person_id": 17, "org_id": 8, "title": "县人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正县级", "note": "主持人大工作"},
    # 曾昭洪
    {"person_id": 18, "org_id": 8, "title": "县人大常委会党组副书记、副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 吴家福
    {"person_id": 19, "org_id": 8, "title": "县人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 杨本环
    {"person_id": 20, "org_id": 8, "title": "县人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 陆光明
    {"person_id": 21, "org_id": 8, "title": "县人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 戴德
    {"person_id": 22, "org_id": 8, "title": "县人大常委会党组成员、副主任、县财政局党组书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 刘凤桃
    {"person_id": 23, "org_id": 8, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 莫卫武
    {"person_id": 24, "org_id": 9, "title": "县政协主席、党组书记", "start": "", "end": "present", "rank": "正县级", "note": "主持政协工作"},
    # 田仁飞
    {"person_id": 25, "org_id": 9, "title": "县政协副主席、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 王国敏
    {"person_id": 26, "org_id": 9, "title": "县政协副主席、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 刘忠燕
    {"person_id": 27, "org_id": 9, "title": "县政协副主席", "start": "", "end": "present", "rank": "副县级", "note": "非党"},
    # 彭皓
    {"person_id": 28, "org_id": 9, "title": "县政协党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 罗敏
    {"person_id": 29, "org_id": 9, "title": "县政协副主席、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 陈国本
    {"person_id": 30, "org_id": 9, "title": "县政协副主席、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 文庆超
    {"person_id": 31, "org_id": 9, "title": "县政协副主席、党组成员", "start": "", "end": "present", "rank": "副县级", "note": ""},
]

RELATIONSHIPS = [
    # ── 核心领导关系 (Core Leadership Relationship) ──
    {
        "person_a": 1, "person_b": 2,
        "type": "党政主要领导",
        "context": "县委书记与县长，党政一把手搭档",
        "overlap_org": "中共平塘县委员会",
        "overlap_period": "至今",
    },
    # ── 县委常委会搭档关系 (Standing Committee Colleagues) ──
    {
        "person_a": 1, "person_b": 3,
        "type": "上下级",
        "context": "县委书记与常务副县长，县委常委会搭档",
        "overlap_org": "中共平塘县委员会常委会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "上下级",
        "context": "县委书记与组织部长，县委常委会搭档",
        "overlap_org": "中共平塘县委员会常委会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "上下级",
        "context": "县委书记与县委办主任，直接上下级",
        "overlap_org": "中共平塘县委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "上下级",
        "context": "县委书记与纪委书记，县委常委会搭档",
        "overlap_org": "中共平塘县委员会常委会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1, "person_b": 9,
        "type": "上下级",
        "context": "县委书记与宣传部长，县委常委会搭档",
        "overlap_org": "中共平塘县委员会常委会",
        "overlap_period": "至今",
    },
    # ── 县政府班子关系 (Government Team) ──
    {
        "person_a": 2, "person_b": 3,
        "type": "上下级",
        "context": "县长与常务副县长，政府班子搭档",
        "overlap_org": "平塘县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "共事",
        "context": "县长与副县长（王波），政府班子同事",
        "overlap_org": "平塘县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2, "person_b": 13,
        "type": "共事",
        "context": "县长与副县长（杨俊程），政府班子同事",
        "overlap_org": "平塘县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2, "person_b": 14,
        "type": "共事",
        "context": "县长与副县长（雷贵桃），政府班子同事",
        "overlap_org": "平塘县人民政府",
        "overlap_period": "至今",
    },
    # ── 四套班子关系 (Four Sets of Leaders) ──
    {
        "person_a": 1, "person_b": 17,
        "type": "联系",
        "context": "县委书记联系人大，与人大主任",
        "overlap_org": "平塘县",
        "overlap_period": "至今",
    },
    {
        "person_a": 1, "person_b": 24,
        "type": "联系",
        "context": "县委书记联系政协，与政协主席",
        "overlap_org": "平塘县",
        "overlap_period": "至今",
    },
]

# fmt: on

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "平塘县_network.db"
GEXF_PATH = STAGING_DIR / "平塘县_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="平塘县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")
