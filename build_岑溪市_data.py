#!/usr/bin/env python3
"""Build script for 岑溪市 (Cenxi City, Wuzhou, Guangxi) leadership network.

Generated: 2026-07-23
Level: 县级市
Province: 广西壮族自治区
Parent City: 梧州市
Targets: 市委书记 & 市长

Research Notes:
  Current Party Secretary: 赵春雷 (b.1981-03, 湖南澧县人, 梧州市工信局局长下派, 2023.11上任)
  Current Mayor: 吴伟华 (b.1972-09, 广西贺州人, 侗族, 在岑溪工作10+年, 2018.05从常务副市长升任)
  Previous Party Secretary: 罗伟雄 (b.1974-10, 广西梧州人, 晋升梧州市委常委、政法委书记)
  Previous Mayor: 罗伟雄(2016-2018) → 吴伟华(2018-)

  Confirmed facts:
  - 赵春雷: 2005-2013梧州市委组织部(人才科科长), 2016-2018藤县组织部长,
    2018-2019市委组织部副部长, 2019-2021市政府副秘书长, 2021-2023市工信局局长
  - 吴伟华: 1993-1994梧州市蝶山区检察院书记员, 约2014到岑溪任常务副市长,
    2018.05升市长.
  - 罗伟雄: 2016.05-2018.05岑溪市长, 2018.05-2023.10岑溪市委书记,
    2023.10晋升梧州市委常委、政法委书记.
  - 欧杰(b.1973-10, 岑溪籍): 曾任梧州市委副秘书长, 2026.03当选岑溪人大主任.
  - 谭永辉(b.1978-09, 湖南衡东): 蒙山县黄村镇镇长→岑溪组织部长→副书记.
  - 万少杰(b.1993-01): 自治区工信厅节能处副处长空降岑溪常委/统战部长/副市长.
  - 覃晋平(b.1986-06, 壮族): 岑溪副市长/常委, 2026.06拟提名县长候选人.
  - 黄振华(b.1973-03, 广西贺州): 梧州市公安局经侦支队长→岑溪副市长/公安局长.
  - 孔斌(b.1972-09, 广西富川, 瑶族): 岑溪常务副市长→苍梧县长(后被查).

  GAPS:
  - 韦学文(政协主席): 来岑溪前完整履历未知
  - 吴伟华: 1994-2014二十年履历空白
  - 徐金良、谭勇球、李培川、韦柳娜、唐钟南(常委): 全部履历待查
  - 覃晋平来岑溪前履历
  - 羽国强(原人大主任)去向

Sources:
  - http://m.gxcounty.com/show-30-180595-0.html (赵春雷任岑溪市委书记)
  - http://m.gxcounty.com/show-30-180403-0.html (赵春雷任前公示)
  - https://www.newton.com.tw/wiki/吳偉華/20373860 (吴伟华简历)
  - https://www.cenxi.cn/ (欧杰当选人大主任 2026-03-04)
  - http://www.gxnews.com.cn/ (欧杰任前公示 2019)
  - http://m.gxcounty.com/show-30-183389-0.html (谭永辉任副书记)
  - http://www.gxcounty.com/zhengwu/rsrm/184740.html (万少杰空降岑溪)
  - http://www.gx.xinhuanet.com/ (覃晋平拟提名县长 2026-06)
  - https://baike.baidu.com/item/黄振华/59248174
  - http://m.gxcounty.com/show-30-184757-0.html (朱璐任副市长)
  - http://m.gxcounty.com/show-30-182306-0.html (林晓通任副市长)
  - http://www.gxcounty.com/zhengwu/rsrm/180274.html (罗伟雄晋升)
  - https://baike.baidu.com/item/孔斌/59249604
  - http://www.gxzx.gov.cn/ (韦学文政协相关)
  - https://www.gxjjw.gov.cn/ (自治区巡视反馈)
"""

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "赵春雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "湖南澧县",
        "education": "大学，法学学士",
        "party_join": "2004年5月",
        "work_start": "2005年3月",
        "current_post": "市委书记",
        "current_org": "岑溪市委",
        "source": "http://m.gxcounty.com/show-30-180595-0.html; http://m.gxcounty.com/show-30-180403-0.html",
    },
    {
        "id": 2,
        "name": "吴伟华",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1972年9月",
        "birthplace": "广西贺州",
        "education": "广西司法学校法律专业，在职研究生（广西区委党校国民经济专业）",
        "party_join": "2000年12月",
        "work_start": "1993年7月",
        "current_post": "市委副书记、市长",
        "current_org": "岑溪市政府",
        "source": "https://www.newton.com.tw/wiki/吳偉華/20373860",
    },
    {
        "id": 3,
        "name": "欧杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "广西岑溪",
        "education": "大学，文学学士",
        "party_join": "1994年11月",
        "work_start": "",
        "current_post": "市人大常委会党组书记、主任",
        "current_org": "岑溪市人大常委会",
        "source": "https://www.cenxi.cn/index.php/2026/03/04/欧杰当选为岑溪市第十七届人民代表大会常务委员会主任/; http://www.gxnews.com.cn/staticpages/20190226/newgx5c7535f9-18073158.shtml",
    },
    {
        "id": 4,
        "name": "韦学文",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席、党组书记",
        "current_org": "岑溪市政协",
        "source": "http://www.gxzx.gov.cn/index.php?a=show&c=index&catid=62&id=55282&m=content",
    },
    {
        "id": 5,
        "name": "谭永辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年9月",
        "birthplace": "湖南衡东",
        "education": "在职研究生，理学学士",
        "party_join": "2003年8月",
        "work_start": "2002年7月",
        "current_post": "市委副书记",
        "current_org": "岑溪市委",
        "source": "http://m.gxcounty.com/show-30-183389-0.html",
    },
    {
        "id": 6,
        "name": "练泽明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记（原）",
        "current_org": "岑溪市委（前任）",
        "source": "https://baike.baidu.com/item/中国共产党岑溪市委员会/62677990",
    },
    {
        "id": 7,
        "name": "覃晋平",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1986年6月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "岑溪市委/岑溪市政府",
        "source": "http://www.gx.xinhuanet.com/20260618/0a84d36cc0dc439b9f49f5513303506f/c.html",
    },
    {
        "id": 8,
        "name": "徐金良",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "岑溪市委",
        "source": "http://www.gxcounty.com/zhengwu/rsrm/184740.html",
    },
    {
        "id": 9,
        "name": "谭勇球",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "岑溪市委",
        "source": "http://www.gxcounty.com/zhengwu/rsrm/184740.html",
    },
    {
        "id": 10,
        "name": "李培川",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "岑溪市委",
        "source": "http://www.gxcounty.com/zhengwu/rsrm/184740.html",
    },
    {
        "id": 11,
        "name": "万少杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1993年1月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、统战部部长、副市长",
        "current_org": "岑溪市委/岑溪市政府",
        "source": "http://www.gxcounty.com/zhengwu/rsrm/184740.html",
    },
    {
        "id": 12,
        "name": "韦柳娜",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "岑溪市委",
        "source": "http://www.gxcounty.com/zhengwu/rsrm/184740.html",
    },
    {
        "id": 13,
        "name": "唐钟南",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "岑溪市委",
        "source": "http://www.gxcounty.com/zhengwu/rsrm/184740.html",
    },
    {
        "id": 14,
        "name": "黄振华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "广西贺州",
        "education": "广西大学工业分析专业",
        "party_join": "1999年7月",
        "work_start": "1994年7月",
        "current_post": "副市长、公安局局长",
        "current_org": "岑溪市政府/公安局",
        "source": "https://baike.baidu.com/item/黄振华/59248174",
    },
    {
        "id": 15,
        "name": "朱璐",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1989年12月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "岑溪市政府",
        "source": "http://m.gxcounty.com/show-30-184757-0.html",
    },
    {
        "id": 16,
        "name": "林晓通",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "岑溪市政府",
        "source": "http://m.gxcounty.com/show-30-182306-0.html",
    },
    {
        "id": 17,
        "name": "陈文强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年11月",
        "birthplace": "广西岑溪",
        "education": "西南大学/经济管理",
        "party_join": "1991年6月",
        "work_start": "1991年11月",
        "current_post": "副市长",
        "current_org": "岑溪市政府",
        "source": "https://baike.so.com/doc/5671300-24925495.html",
    },
    {
        "id": 18,
        "name": "羽国强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原人大常委会主任",
        "current_org": "岑溪市人大常委会（前任）",
        "source": "http://cenxi.pawz.gov.cn/article_show.php?id=16107",
    },
    {
        "id": 19,
        "name": "罗伟雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "广西梧州",
        "education": "研究生，广西大学",
        "party_join": "1994年12月",
        "work_start": "1995年",
        "current_post": "梧州市委常委、政法委书记（前任岑溪市委书记）",
        "current_org": "梧州市委",
        "source": "http://www.gxcounty.com/zhengwu/rsrm/180274.html",
    },
    {
        "id": 20,
        "name": "孔斌",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "1972年9月",
        "birthplace": "广西富川",
        "education": "在职研究生，重庆交通大学",
        "party_join": "1995年12月",
        "work_start": "1994年7月",
        "current_post": "原岑溪市常务副市长（已调任/被查）",
        "current_org": "岑溪市政府（原）",
        "source": "https://baike.baidu.com/item/孔斌/59249604",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中国共产党岑溪市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共梧州市委员会",
        "location": "岑溪市",
    },
    {
        "id": 2,
        "name": "岑溪市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "梧州市人民政府",
        "location": "岑溪市",
    },
    {
        "id": 3,
        "name": "岑溪市人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "梧州市人大常委会",
        "location": "岑溪市",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议岑溪市委员会",
        "type": "政协",
        "level": "县级",
        "parent": "梧州市政协",
        "location": "岑溪市",
    },
    {
        "id": 5,
        "name": "岑溪市公安局",
        "type": "政府",
        "level": "科级",
        "parent": "岑溪市人民政府",
        "location": "岑溪市",
    },
    {
        "id": 6,
        "name": "梧州市工业和信息化局",
        "type": "政府",
        "level": "正处级",
        "parent": "梧州市人民政府",
        "location": "梧州市",
    },
    {
        "id": 7,
        "name": "梧州市委组织部",
        "type": "党委",
        "level": "正处级",
        "parent": "中共梧州市委员会",
        "location": "梧州市",
    },
    {
        "id": 8,
        "name": "藤县县委",
        "type": "党委",
        "level": "县级",
        "parent": "中共梧州市委员会",
        "location": "藤县",
    },
    {
        "id": 9,
        "name": "梧州市人民政府办公室",
        "type": "政府",
        "level": "正处级",
        "parent": "梧州市人民政府",
        "location": "梧州市",
    },
    {
        "id": 10,
        "name": "中共梧州市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共广西壮族自治区委员会",
        "location": "梧州市",
    },
    {
        "id": 11,
        "name": "蒙山县黄村镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "蒙山县人民政府",
        "location": "蒙山县",
    },
    {
        "id": 12,
        "name": "广西壮族自治区工业和信息化厅",
        "type": "政府",
        "level": "厅级",
        "parent": "广西壮族自治区人民政府",
        "location": "南宁市",
    },
    {
        "id": 13,
        "name": "梧州市公安局",
        "type": "政府",
        "level": "正处级",
        "parent": "梧州市人民政府",
        "location": "梧州市",
    },
    {
        "id": 14,
        "name": "梧州市生态环境局",
        "type": "政府",
        "level": "正处级",
        "parent": "梧州市人民政府",
        "location": "梧州市",
    },
]

POSITIONS = [
    # 赵春雷
    {"person_id": 1, "org_id": 7, "title": "梧州市委组织部人才工作科科长、市紧缺人才储备中心主任", "start_date": "2013", "end_date": "2016.05", "rank": "正科级", "note": "此前在梧州市委组织部办公室主任等岗"},
    {"person_id": 1, "org_id": 8, "title": "藤县县委常委、组织部部长", "start_date": "2016.05", "end_date": "2018.03", "rank": "副处级", "note": "首次下县任职"},
    {"person_id": 1, "org_id": 7, "title": "梧州市委组织部副部长", "start_date": "2018.03", "end_date": "2019.03", "rank": "副处级", "note": "回市直机关"},
    {"person_id": 1, "org_id": 9, "title": "梧州市人民政府副秘书长、办公室副主任", "start_date": "2019.03", "end_date": "2021.08", "rank": "副处级", "note": "离开组织系统"},
    {"person_id": 1, "org_id": 6, "title": "梧州市工业和信息化局局长、党组书记", "start_date": "2021.08", "end_date": "2023.11", "rank": "正处级", "note": "来岑溪前最后职务"},
    {"person_id": 1, "org_id": 1, "title": "岑溪市委书记", "start_date": "2023.11", "end_date": "present", "rank": "正处级", "note": "当前职务"},
    # 吴伟华
    {"person_id": 2, "org_id": 9, "title": "梧州市蝶山区人民检察院书记员", "start_date": "1993.07", "end_date": "1994.09", "rank": "科员", "note": "第一份工作"},
    {"person_id": 2, "org_id": 2, "title": "岑溪市委常委、常务副市长", "start_date": "2014", "end_date": "2018.05", "rank": "副处级", "note": "1994-2014年履历空缺"},
    {"person_id": 2, "org_id": 2, "title": "岑溪市委副书记、市长", "start_date": "2018.05", "end_date": "present", "rank": "正处级", "note": "从常务副市长升任"},
    # 欧杰
    {"person_id": 3, "org_id": 10, "title": "梧州市委副秘书长、办公室副主任、督查室主任", "start_date": "", "end_date": "2025", "rank": "正处级", "note": "2019年2月任前公示确认"},
    {"person_id": 3, "org_id": 3, "title": "岑溪市人大常委会党组书记、主任", "start_date": "2026.03", "end_date": "present", "rank": "正处级", "note": "2025年12月先任党组书记，2026.03当选主任"},
    # 韦学文
    {"person_id": 4, "org_id": 4, "title": "岑溪市政协主席、党组书记", "start_date": "2022.09", "end_date": "present", "rank": "正处级", "note": "2022年9月已在任，来岑溪前履历待查"},
    # 谭永辉
    {"person_id": 5, "org_id": 11, "title": "蒙山县黄村镇党委副书记、镇长", "start_date": "", "end_date": "2022", "rank": "正科级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "岑溪市委常委、组织部部长", "start_date": "2022.09", "end_date": "2025.06", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "岑溪市委副书记", "start_date": "2025.06", "end_date": "present", "rank": "副处级", "note": "进一步使用"},
    # 练泽明（原副书记）
    {"person_id": 6, "org_id": 1, "title": "岑溪市委副书记（原）", "start_date": "", "end_date": "", "rank": "副处级", "note": "已在2025年12月理论学习中心组名单中未出现"},
    # 覃晋平
    {"person_id": 7, "org_id": 1, "title": "岑溪市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026.06拟提名为县长候选人"},
    # 万少杰
    {"person_id": 11, "org_id": 12, "title": "自治区工信厅节能与综合利用处副处长", "start_date": "", "end_date": "2025.12", "rank": "副处级", "note": "来岑溪前最后职务，空降至基层"},
    {"person_id": 11, "org_id": 1, "title": "岑溪市委常委、统战部部长", "start_date": "2025.12", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "岑溪市副市长（兼）", "start_date": "2025.12", "end_date": "present", "rank": "副处级", "note": ""},
    # 黄振华
    {"person_id": 14, "org_id": 13, "title": "梧州市公安局经济犯罪侦查支队支队长", "start_date": "2020.04", "end_date": "2021.06", "rank": "正科级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "岑溪市副市长、公安局局长", "start_date": "2021.08", "end_date": "present", "rank": "副处级", "note": ""},
    # 朱璐
    {"person_id": 15, "org_id": 14, "title": "梧州市生态环境局土壤生态环境科科长", "start_date": "", "end_date": "2026.01", "rank": "正科级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "岑溪市副市长", "start_date": "2026.01", "end_date": "present", "rank": "副处级", "note": ""},
    # 林晓通
    {"person_id": 16, "org_id": 1, "title": "岑溪市委办公室副主任", "start_date": "2013.01", "end_date": "2013.09", "rank": "副科级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "梨木镇党委书记、大业镇党委书记", "start_date": "2013.09", "end_date": "2025", "rank": "正科级", "note": "从乡镇党委书记升任副市长"},
    {"person_id": 16, "org_id": 2, "title": "岑溪市副市长", "start_date": "2025", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈文强
    {"person_id": 17, "org_id": 2, "title": "岑溪市马路镇党委副书记、镇长", "start_date": "2012", "end_date": "2019", "rank": "正科级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "岑溪市副市长", "start_date": "2019", "end_date": "present", "rank": "副处级", "note": ""},
    # 孔斌（原常务副市长）
    {"person_id": 20, "org_id": 2, "title": "岑溪市委常委、常务副市长", "start_date": "2018.06", "end_date": "2021.06", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "苍梧县委副书记、县长", "start_date": "2021.08", "end_date": "2025.06", "rank": "正处级", "note": "后被查"},
    # 罗伟雄（前任书记）
    {"person_id": 19, "org_id": 2, "title": "岑溪市市长", "start_date": "2016.05", "end_date": "2018.05", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 1, "title": "岑溪市委书记", "start_date": "2018.05", "end_date": "2023.10", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 10, "title": "梧州市委常委、政法委书记", "start_date": "2023.10", "end_date": "present", "rank": "副厅级", "note": "晋升"},
]

RELATIONSHIPS = [
    # 赵春雷—罗伟雄：前后任市委书记
    {"person_a": 1, "person_b": 19, "type": "predecessor_successor", "context": "赵春雷接替罗伟雄任岑溪市委书记", "overlap_org": "岑溪市委", "overlap_period": "2023.10-2023.11"},
    # 赵春雷—吴伟华：书记-市长搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记与市长党政一把手搭档", "overlap_org": "岑溪市四家班子", "overlap_period": "2023.11至今"},
    # 吴伟华—罗伟雄：前后任市长
    {"person_a": 2, "person_b": 19, "type": "predecessor_successor", "context": "吴伟华接替罗伟雄任岑溪市长", "overlap_org": "岑溪市政府", "overlap_period": "2018.05"},
    # 赵春雷—谭永辉：书记-副书记/原组织部长
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "赵春雷任书记时谭永辉先任组织部长后任副书记", "overlap_org": "岑溪市委", "overlap_period": "2023.11至今"},
    # 万少杰—赵春雷：自治区空降下级与书记
    {"person_a": 11, "person_b": 1, "type": "superior_subordinate", "context": "万少杰从自治区工信厅空降岑溪任统战部长/副市长，为赵春雷下属", "overlap_org": "岑溪市委/政府", "overlap_period": "2025.12至今"},
    # 黄振华—赵春雷：公安局长为书记下属
    {"person_a": 14, "person_b": 1, "type": "superior_subordinate", "context": "黄振华（公安局长）为赵春雷下属", "overlap_org": "岑溪市政府", "overlap_period": "2023.11至今"},
    # 黄振华—吴伟华：公安局长为市长下属
    {"person_a": 14, "person_b": 2, "type": "superior_subordinate", "context": "黄振华为吴伟华下属", "overlap_org": "岑溪市政府", "overlap_period": "2021.08至今"},
    # 孔斌—吴伟华：曾为常务副手
    {"person_a": 20, "person_b": 2, "type": "overlap", "context": "孔斌曾为吴伟华常务副手（常务副市长）", "overlap_org": "岑溪市政府", "overlap_period": "2018.06-2021.06"},
    # 谭永辉—吴伟华：副书记-市长共事
    {"person_a": 5, "person_b": 2, "type": "overlap", "context": "谭永辉先任组织部长后任副书记，与市长吴伟华长期共事", "overlap_org": "岑溪市委/政府", "overlap_period": "2022.09至今"},
    # 欧杰—赵春雷：人大主任-书记
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "欧杰任人大主任，与赵春雷在岑溪共事", "overlap_org": "岑溪市四家班子", "overlap_period": "2026.03至今"},
]

# fmt: on

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

DB_PATH = DATABASE_DIR / "岑溪市_network.db"
GEXF_PATH = GRAPH_DIR / "岑溪市_network.gexf"


def main() -> None:
    run_build(
        slug="岑溪市",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )


if __name__ == "__main__":
    main()
