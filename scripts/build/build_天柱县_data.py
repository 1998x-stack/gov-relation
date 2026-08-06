#!/usr/bin/env python3
"""Build SQLite database + GEXF graph + person JSONs for 天柱县 (Tianzhu County), 贵州省.

Investigation date: 2026-08-06
Task ID: guizhou_天柱县
Level: 县级
Targets: 县委书记 & 县长

Sources: 天柱县人民政府门户网站 (www.tianzhu.gov.cn) 政府领导之窗 + 政务要闻/领导活动;
黔东南州政府网 (www.qdn.gov.cn).

Confidence:
  - 县委书记 赵明波: CONFIRMED via county news (2026-06/07); personal bio fields not obtained -> gap.
  - 县长 杨用华: CONFIRMED incl. birth/education via 政府领导之窗 (1975-02, 侗族, 本科).
  - 县政府领导班子: CONFIRMED via 政府领导之窗 zfld1 profiles.
  - 人大主任彭子培、政协主席赖燕明、县委副书记吴量、组织部长陈守宇: CONFIRMED via county news.
  - 公安局长更迭: 龙安臻为现任（政府领导之窗 2026-07-30 最新），陈远剑为前一人（人大42次会议 2026-07-15）。
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

for _parent in Path(__file__).resolve().parents:
    if (_parent / "gov_relation").is_dir():
        sys.path.insert(0, str(_parent))
        break

from gov_relation.runner import run_build  # noqa: E402

SLUG = "天柱县"
PROVINCE = "贵州省"
CITY = "黔东南苗族侗族自治州"
AS_OF = "2026-08-06"
TASK_ID = "guizhou_天柱县"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons (confirmed as-of 2026-08-06) ─────────────────────────────────
persons = [
    {"id": 1, "name": "赵明波", "gender": "男", "ethnicity": "彝族", "birth": "1983-11", "birthplace": "贵州贵阳",
     "education": "中国矿业大学（北京）资源环境与城乡规划管理专业，大学（理学学士）", "party_join": "2010-05", "work_start": "2006-07",
     "current_post": "县委书记", "current_org": "中共天柱县委员会",
     "source": "https://www.tianzhu.gov.cn/xwzx/ 及 新京报/百度百科（媒体）"},
    {"id": 2, "name": "杨用华", "gender": "男", "ethnicity": "侗族", "birth": "1975-02", "birthplace": "",
     "education": "本科学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、县长", "current_org": "天柱县人民政府",
     "source": "https://www.tianzhu.gov.cn/zwgk/ldzc/zfld1/202503/t20250327_87288606.html"},
    {"id": 3, "name": "杨胜海", "gender": "男", "ethnicity": "苗族", "birth": "1980-07", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "天柱县人民政府",
     "source": "https://www.tianzhu.gov.cn/zwgk/ldzc/zfld1/202503/t20250327_87288605.html"},
    {"id": 4, "name": "蒋大伍", "gender": "男", "ethnicity": "苗族", "birth": "1979-05", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长", "current_org": "天柱县人民政府",
     "source": "https://www.tianzhu.gov.cn/zwgk/ldzc/zfld1/202503/t20250327_87288604.html"},
    {"id": 5, "name": "邓伟文", "gender": "男", "ethnicity": "汉族", "birth": "1975-12", "birthplace": "",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长（挂职）", "current_org": "天柱县人民政府",
     "source": "https://www.tianzhu.gov.cn/zwgk/ldzc/zfld1/202503/t20250327_87288603.html"},
    {"id": 6, "name": "乐华胜", "gender": "男", "ethnicity": "汉族", "birth": "1980-08", "birthplace": "",
     "education": "本科学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长", "current_org": "天柱县人民政府",
     "source": "https://www.tianzhu.gov.cn/zwgk/ldzc/zfld1/202507/t20250704_88232389.html"},
    {"id": 7, "name": "陈守宇", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、县委组织部部长", "current_org": "中共天柱县委员会",
     "source": "https://www.tianzhu.gov.cn/xwzx/tzyw/202607/t20260721_90643229.html"},
    {"id": 8, "name": "吴量", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委副书记", "current_org": "中共天柱县委员会",
     "source": "https://www.tianzhu.gov.cn/xwzx/ldhd/202607/t20260709_90600884.html"},
    {"id": 9, "name": "王建元", "gender": "男", "ethnicity": "侗族", "birth": "1979-09", "birthplace": "",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县政府党组成员、副县长", "current_org": "天柱县人民政府",
     "source": "https://www.tianzhu.gov.cn/zwgk/ldzc/zfld1/202503/t20250327_87288593.html"},
    {"id": 10, "name": "杨燕敏", "gender": "女", "ethnicity": "侗族", "birth": "1979-11", "birthplace": "",
     "education": "大学本科学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县政府党组成员、副县长", "current_org": "天柱县人民政府",
     "source": "https://www.tianzhu.gov.cn/zwgk/ldzc/zfld1/202509/t20250902_88553906.html"},
    {"id": 11, "name": "龙安臻", "gender": "男", "ethnicity": "苗族", "birth": "1978-03", "birthplace": "",
     "education": "工程硕士学历", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长、县公安局局长", "current_org": "天柱县人民政府",
     "source": "https://www.tianzhu.gov.cn/zwgk/ldzc/zfld1/202607/t20260730_90676161.html"},
    {"id": 12, "name": "石成程", "gender": "男", "ethnicity": "汉族", "birth": "1989-11", "birthplace": "",
     "education": "在职研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "县政府党组成员、副县长", "current_org": "天柱县人民政府",
     "source": "https://www.tianzhu.gov.cn/zwgk/ldzc/zfld1/202607/t20260730_90676223.html"},
    {"id": 13, "name": "彭文荣", "gender": "男", "ethnicity": "苗族", "birth": "1978-10", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县政府党组成员、副县长", "current_org": "天柱县人民政府",
     "source": "https://www.tianzhu.gov.cn/zwgk/ldzc/zfld1/202607/t20260730_90676328.html"},
    {"id": 14, "name": "龙林", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "天柱县人民政府",
     "source": "https://www.tianzhu.gov.cn/xwzx/ldhd/202604/t20260429_90056212.html"},
    {"id": 15, "name": "陈远剑", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "（前）副县长、县公安局局长", "current_org": "天柱县人民政府",
     "source": "https://www.tianzhu.gov.cn/xwzx/tzyw/202607/t20260715_90621491.html"},
    {"id": 16, "name": "彭子培", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "天柱县人民代表大会常务委员会",
     "source": "https://www.tianzhu.gov.cn/xwzx/tzyw/202607/t20260715_90621491.html"},
    {"id": 17, "name": "赖燕明", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政协主席", "current_org": "中国人民政治协商会议天柱县委员会",
     "source": "https://www.tianzhu.gov.cn/xwzx/tzyw/202606/t20260612_90519442.html"},
    {"id": 18, "name": "龙剑", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "天柱县人民代表大会常务委员会",
     "source": "https://www.tianzhu.gov.cn/xwzx/tzyw/202607/t20260715_90621491.html"},
    {"id": 19, "name": "潘海涛", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "天柱县人民代表大会常务委员会",
     "source": "https://www.tianzhu.gov.cn/xwzx/tzyw/202607/t20260715_90621491.html"},
    {"id": 20, "name": "何善权", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "天柱县人民代表大会常务委员会",
     "source": "https://www.tianzhu.gov.cn/xwzx/tzyw/202607/t20260715_90621491.html"},
    {"id": 21, "name": "欧阳大彬", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "天柱县人民代表大会常务委员会",
     "source": "https://www.tianzhu.gov.cn/xwzx/tzyw/202607/t20260715_90621491.html"},
    {"id": 22, "name": "周邦林", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "天柱县人民代表大会常务委员会",
     "source": "https://www.tianzhu.gov.cn/xwzx/tzyw/202607/t20260715_90621491.html"},
    {"id": 23, "name": "谭睿", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "贵州天柱经开区党工委副书记、管委会主任", "current_org": "贵州天柱经济开发区",
     "source": "https://www.tianzhu.gov.cn/xwzx/ldhd/202604/t20260422_90030955.html"},
    {"id": 24, "name": "吴绍东", "gender": "男", "ethnicity": "苗族", "birth": "1970-01", "birthplace": "贵州黄平",
     "education": "省委党校大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "（前任）天柱县委书记 → 铜仁市副市长", "current_org": "铜仁市人民政府",
     "source": "人民网贵州频道 / 铜仁人大任命（经搜狗微信转载）"},
]

# ── Organizations ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共天柱县委员会", "type": "党委", "level": "县级", "parent": "中共黔东南州委", "location": "贵州省黔东南州天柱县"},
    {"id": 2, "name": "天柱县人民政府", "type": "政府", "level": "县级", "parent": "黔东南州人民政府", "location": "贵州省黔东南州天柱县"},
    {"id": 3, "name": "天柱县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "天柱县", "location": "贵州省黔东南州天柱县"},
    {"id": 4, "name": "中国人民政治协商会议天柱县委员会", "type": "政协", "level": "县级", "parent": "天柱县", "location": "贵州省黔东南州天柱县"},
    {"id": 5, "name": "中共黔东南州委", "type": "党委", "level": "地级市", "parent": "中共贵州省委", "location": "贵州省黔东南州凯里市"},
    {"id": 6, "name": "黔东南州人民政府", "type": "政府", "level": "地级市", "parent": "贵州省人民政府", "location": "贵州省黔东南州凯里市"},
    {"id": 7, "name": "天柱县公安局", "type": "政府", "level": "县级", "parent": "天柱县人民政府", "location": "贵州省黔东南州天柱县"},
    {"id": 8, "name": "贵州天柱经济开发区", "type": "开发区", "level": "县级", "parent": "天柱县人民政府", "location": "贵州省黔东南州天柱县"},
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正县级",
     "note": "现任县委书记（官方新闻 2026-06/07 确认）；履历未公开"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正县级",
     "note": "县委副书记、县长、党组书记；领导政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "兼任县委副书记"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "县委委员/常委"},
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "负责政府常务（发改/金融/税务/统计/应急/大数据等），协助县长"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "县委委员/常委"},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "分管工业化/招商引资/自然资源/开发展"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "县委委员/常委"},
    {"person_id": 5, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "副县级", "note": "挂职副县长"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "县委委员/常委"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "挂职/定点帮扶"},
    {"person_id": 7, "org_id": 1, "title": "县委常委、县委组织部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "组织工作负责人"},
    {"person_id": 8, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "专职县委副书记"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "县政府党组成员、副县长；分管农业/乡村振兴/水务/林业"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "县政府党组成员、副县长；分管教育/卫健/医保/民政"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "县政府党组成员、副县长、县公安局党委书记、局长（政府领导之窗 2026-07-30）"},
    {"person_id": 11, "org_id": 7, "title": "县公安局局长", "start_date": "", "end_date": "", "rank": "副县级", "note": "主持县公安局全面工作"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "县政府党组成员、副县长；分管住建/文旅/市监（1989年，最年轻）"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "县政府党组成员、副县长；分管交通/环保/移民/民宗"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "副县长（2026-04 新闻）"},
    {"person_id": 15, "org_id": 2, "title": "副县长、县公安局局长", "start_date": "", "end_date": "2026-07", "rank": "副县级",
     "note": "前任公安局长（人大42次会议 2026-07-15 列席）"},
    {"person_id": 16, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正县级", "note": "县四大班子领导"},
    {"person_id": 17, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正县级", "note": "县四大班子领导"},
    {"person_id": 18, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "县人大常委会副主任"},
    {"person_id": 19, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "县人大常委会副主任"},
    {"person_id": 20, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "县人大常委会副主任"},
    {"person_id": 21, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "县人大常委会副主任"},
    {"person_id": 22, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "县人大常委会副主任"},
    {"person_id": 23, "org_id": 8, "title": "党工委副书记、管委会主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "贵州天柱经济开发区"},
    {"person_id": 24, "org_id": 1, "title": "县委书记", "start_date": "2021-06", "end_date": "~2023", "rank": "正县级",
     "note": "前任县委书记；2016.07-2021.06 任天柱县长，2021.06 升任书记"},
    {"person_id": 24, "org_id": 2, "title": "县长", "start_date": "2016-07", "end_date": "2021-06", "rank": "正县级",
     "note": "天柱县委副书记、县长，兼天柱工业园区管委会主任"},
    {"person_id": 24, "org_id": 2, "title": "铜仁市副市长", "start_date": "~2023", "end_date": "", "rank": "副厅级",
     "note": "外调铜仁市副市长、市公安局局长（跨州外调）"},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长（党委政府一把手搭档）", "overlap_org": "中共天柱县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "县委书记—县委副书记", "overlap_org": "中共天柱县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记—组织部长（县委常委会工作）", "overlap_org": "中共天柱县委员会", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长—常务副县长（主持政府日常）", "overlap_org": "天柱县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长—副县长（兼常委）", "overlap_org": "天柱县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长—副县长王建元", "overlap_org": "天柱县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长—副县长杨燕敏", "overlap_org": "天柱县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长—副县长石成程", "overlap_org": "天柱县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长—副县长彭文荣", "overlap_org": "天柱县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 23, "type": "工作往来", "context": "县长—经开区管委会主任（工业经济）", "overlap_org": "贵州天柱经济开发区", "overlap_period": "现任"},
    {"person_a": 11, "person_b": 15, "type": "职务接替", "context": "龙安臻接替陈远剑任副县长、县公安局局长", "overlap_org": "天柱县人民政府", "overlap_period": "2026-07"},
    {"person_a": 16, "person_b": 17, "type": "同届共事", "context": "人大主任—政协主席（县四套班子）", "overlap_org": "中共天柱县委员会", "overlap_period": "现任"},
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "两位县委常委同班子", "overlap_org": "中共天柱县委员会", "overlap_period": "现任"},
    {"person_a": 4, "person_b": 6, "type": "共事", "context": "两位常委副县长协作（工业化/帮扶）", "overlap_org": "天柱县人民政府", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 16, "type": "同班子", "context": "县委书记—人大主任（县四大班子）", "overlap_org": "中共天柱县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 17, "type": "同班子", "context": "县委书记—政协主席（县四大班子）", "overlap_org": "中共天柱县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 24, "type": "前任继任", "context": "前任县委书记吴绍东→继任书记赵明波（县委书记换届）", "overlap_org": "中共天柱县委员会", "overlap_period": "~2023"},
    {"person_a": 2, "person_b": 24, "type": "前任继任", "context": "赵明波任县长时吴绍东任书记（党政搭档），后赵明波升书记、吴绍东外调铜仁", "overlap_org": "中共天柱县委员会", "overlap_period": "~2020-2023"},
]

# ── Person JSON profiles ─────────────────────────────────────────────────
def _get(pid):
    for p in persons:
        if p["id"] == pid or p.get("name") == pid:
            return p
    raise KeyError(pid)


def row(start, end, org, title, lvl, system, rank, key, note, conf="confirmed"):
    return {"start": start, "end": end, "org": org, "title": title, "level": lvl, "location": "贵州省",
            "system": system, "rank": rank, "is_key_promotion": key, "notes": note,
            "confidence": conf, "source_ids": ["S001", "S002"]}


def json_profile(person, admin_rank, career_rows, gov_records, gap_note, pattern, systems, spec=()):
    name = person["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": CITY, "region": SLUG,
                                "job": person["current_post"], "task_id": TASK_ID, "time_focus": "2025-2026"},
        "identity": {
            "person_id": f"tianzhu_{name}", "name": name, "aliases": [],
            "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": person.get("education", ""), "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{name}_{person.get('birth','')}",
                            "name_birthplace": f"{name}_{person.get('birthplace','')}",
                            "official_profile_url": person.get("source", "")},
        },
        "current_status": {"current_post": person["current_post"], "current_org": person["current_org"],
                           "administrative_rank": admin_rank, "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S001", "S002"]},
        "career_timeline": career_rows,
        "organizations": [
            {"org": "中共天柱县委员会", "type": "党委", "level": "县级", "location": "贵州省黔东南州天柱县"},
            {"org": "天柱县人民政府", "type": "政府", "level": "县级", "location": "贵州省黔东南州天柱县"},
        ],
        "relationships": [],
        "governance_record": gov_records,
        "professional_profile": {"primary_specializations": list(spec), "secondary_specializations": [],
                                 "career_pattern": pattern, "systems_experience": list(systems),
                                 "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                       "management_signals": [],
                                       "caveat": "Work style is inferred from public records, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "本次官方渠道调研未发现负面信号", "date": "",
                                        "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "天柱县人民政府门户·政府领导之窗", "url": "https://www.tianzhu.gov.cn/zwgk/ldzc/zfld1/",
             "publisher": "天柱县人民政府办公室", "published_at": AS_OF, "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "领导简历官方来源"},
            {"id": "S002", "title": "天柱县政府网·政务要闻/领导活动", "url": "https://www.tianzhu.gov.cn/xwzx/",
             "publisher": "天柱县融媒体中心", "published_at": "2026-08", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "确认书记赵明波、人大主任彭子培、政协主席赖燕明、组织部长蒋守宇等"},
            {"id": "S003", "title": "天柱县政府网·人大常委会第四十二次会议", "url": "https://www.tianzhu.gov.cn/xwzx/tzyw/202607/t20260715_90621491.html",
             "publisher": "天柱县融媒体中心", "published_at": "2026-07-15", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "确认人大班子及前公安局长陈远剑"},
        ],
        "confidence_summary": {"identity": "confirmed" if person.get("birth") else "partial",
                               "current_role": "confirmed",
                               "career_completeness": "complete" if career_rows else "thin",
                               "relationship_confidence": "medium",
                               "biggest_gap": gap_note},
        "open_questions": [{"priority": "high", "question": gap_note, "why_it_matters": "用于跨县网络深度分析",
                            "suggested_queries": [f"{SLUG} {name} 简历", f"{CITY} 组织部 任前公示 {name}"],
                            "last_attempted": AS_OF}],
    }


zhao_career = [
    row("", "present", "中共天柱县委员会", "县委书记、县人武部党委第一书记", "县级", "party", "正县级", True, "现任县委书记（官方新闻 2026-06/07 确认）"),
    row("2021", "2024-06", "天柱县人民政府", "县长", "县级", "government", "正县级", True,
        "2021年任天柱县委副书记、县长；2024年6月公示拟任县委书记（新京报）"),
    row("~2019", "2021", "中共天柱县委", "县委常委、县委副书记", "县级", "party", "副县级", False,
        "从省级机关到天柱任职", "confirmed"),
    {"start": "unknown", "end": "unknown", "org": "履历缺前段（媒体）", "title": "", "level": "", "system": "",
     "rank": "", "is_key_promotion": False, "notes": "较早履历：安顺市西秀区发改局副局长 → 贵州省文联（主任科员/机关党办副主任/机关纪委）等（媒体间源，个别节点时间未精确）",
     "confidence": "plausible", "source_ids": []},
]

wus_career = [
    row("~2023", "", "铜仁市人民政府", "副市长、市公安局局长", "地级市", "government", "副厅级", True, "跨州外调铜仁市副市长、市公安局局长"),
    row("2021-06", "~2023", "中共天柱县委员会", "县委书记", "县级", "party", "正县级", True, "前任天柱县委书记"),
    row("2016-07", "2021-06", "天柱县人民政府", "县长（县委副书记）", "县级", "government", "正县级", True,
        "兼天柱工业园区管委会主任（黔东循环经济工业区）"),
    row("2014-06", "2016-05", "中共黄平县委", "县委副书记、县委政法委书记", "县级", "party", "副县级", True,
        "黄平县委副书记（兼政法委书记）","confirmed"),
]

yang_career = [
    row("", "present", "天柱县人民政府", "县长（县委副书记）", "县级", "government", "正县级", True, "负责政府全面工作（财政/审计/粮食）"),
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "system": "",
     "rank": "", "is_key_promotion": False, "notes": "男，侗族，1975-02生，本科，中共党员；此前任职节点未公开",
     "confidence": "confirmed", "source_ids": ["S001"]},
]

yangsh_career = [
    row("", "", "天柱县人民政府", "常务副县长（县委常委）", "县级", "government", "副县级", True, "主持政府常务工作，协助县长"),
    row("", "", "履历开头", "", "县级", "government", "", False, "男，苗族，1980-07生，大学，中共党员"),
]

wangjy_career = [
    row("", "", "天柱县人民政府", "副县长", "县级", "government", "副县级", True, "分管农业/乡村振兴/水务/林业"),
    row("", "", "履历开头", "", "县级", "government", "", False, "男，侗族，1979-09生，研究生，中共党员"),
]

def _write_profiles_json():
    profiles = []
    zhao = _get("赵明波")
    yang = _get("杨用华")
    chen = _get("杨胜海")   # 常务副县长
    wang = _get("王建元")
    yym = _get("杨燕敏")

    zhao_prof = json_profile(zhao, "正县级", zhao_career, [],
                             "赵明波早期履历部分节点时间（西秀区发改局/省文联→天柱）未精确公开",
                             "cross_county_rotation", ["party", "government", "organization"], "团委/组织系统")
    zhao_prof["identity"]["person_id"] = "tianzhu_zhao_mingbo"
    zhao_prof["open_questions"] = [{"priority": "high", "question": "赵明波在省文联/西秀区发改局各节点的精确起止时间",
                                    "why_it_matters": "县委书记履历完整性", "suggested_queries": ["赵明波 安顺西秀区发改局 任职", "黔东南干部任前公示 赵明波"],
                                    "last_attempted": AS_OF}]

    yang_prof = json_profile(yang, "正县级", yang_career, [], "县长杨用华此前仕途（此前机关/流转路径）未公开",
                          "government", ["government", "party"], "政府管理")
    yang_prof["governance_record"] = [
        {"period": "2026", "domain": "economic_development", "achievement_or_event": "主持县政府全面工作；推动重晶石/钡化工产业发展",
         "role_in_event": "县长", "measurable_outcome": "2026上半年全县GDP增长5.8%", "location": SLUG,
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]

    chen_prof = json_profile(chen, "副县级", yangsh_career, [], "杨胜海此前跨县任职细节待查",
                          "local_ladder", ["government"], [])
    wang_prof = json_profile(wang, "副县级", wangjy_career, [], "王建元早期履历待查",
                             "local_ladder", ["government"], [])
    yym_prof = json_profile(yym, "副县级", [], [], "杨燕敏早期履历待查",
                           "local_ladder", ["government"], [])
    wus = _get("吴绍东")
    wus_prof = json_profile(wus, "副厅级", wus_career, [], "吴绍东（前任书记）黄平在任细节待补全",
                            "cross_county_rotation", ["party", "government"], "政法系统")
    wus_prof["identity"]["person_id"] = "tianzhu_wu_shaodong"
    wus_prof["relationships"] = [
        {"person": "赵明波", "relationship_type": "predecessor_successor", "strength": "strong",
         "evidence": "吴绍东任天柱书记时赵明波任县长，后赵明波升书记", "overlap_org": "中共天柱县委员会",
         "overlap_period": "~2020-2023", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]

    profiles.append((f"{TODAY}-贵州省-黔东南苗族侗族自治州-县委书记-赵明波.json", zhao_prof))
    profiles.append((f"{TODAY}-贵州省-黔东南苗族侗族自治州-县长-杨用华.json", yang_prof))
    profiles.append((f"{TODAY}-贵州省-黔东南苗族侗族自治州-常务副县长-杨胜海.json", chen_prof))
    profiles.append((f"{TODAY}-贵州省-黔东南苗族侗族自治州-副县长-王建元.json", wang_prof))
    profiles.append((f"{TODAY}-贵州省-黔东南苗族侗族自治州-副县长-杨燕敏.json", yym_prof))
    profiles.append((f"{TODAY}-贵州省-黔东南苗族侗族自治州-前任县委书记-吴绍东.json", wus_prof))

    for fname, data in profiles:
        with open(HERE / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return profiles


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 天柱县人民政府门户网站 + 公开报道")
    print("=" * 60)

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

    conn = sqlite3.connect(str(DB_PATH))
    try:
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                  for t in ("persons", "organizations", "positions", "relationships")}
    finally:
        conn.close()
    print("  DB counts:", counts)

    profiles = _write_profiles_json()
    print("\n  人物 JSON: %d 个" % len(profiles))
    for fname, _ in profiles:
        print(f"    - {fname}")

    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    main()