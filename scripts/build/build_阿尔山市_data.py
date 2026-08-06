#!/usr/bin/env python3
"""阿尔山市领导班子关系网络数据生成脚本.

核心人物：市委书记 耿浩；市委副书记、市长 额日贺木图；前任书记 杨永久（盟人大工委副主任兼）；
前任市长 李贺、王晓欢等。
行政归属：内蒙古自治区兴安盟下辖县级市，2026年建市三十周年(1996建市)。
证据来源：阿尔山市人民政府官网(www.aes.gov.cn)领导之窗、市政府领导简历页、
第七届人大常委会第二十九次会议公告(2026-07-16)、2026年政府工作报告(2026-01-13，
市长额日贺木图作)、市委常委会/调研新闻(2026-06~08)等。
置信度标注：confirmed=官网/任免文件；plausible=可信媒体/新闻；unverified=待补线索。
"""

import os
import sys
import sqlite3  # noqa: F401  (standard library; DB written via gov_relation.schema)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

slug = "阿尔山市"

DB_PATH = DATABASE_DIR / f"{slug}_network.db"
GEXF_PATH = GRAPH_DIR / f"{slug}_network.gexf"

# ---------------------------------------------------------------------------
# persons
# ---------------------------------------------------------------------------
persons = [
    # ---- 现任主官 ----
    {"id": 1, "name": "耿浩", "gender": "待查", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委书记", "current_org": "中共阿尔山市委员会",
     "source": "http://www.aes.gov.cn/aes/2026-07/31/article_2026073108180845407.html"},
    {"id": 2, "name": "额日贺木图", "gender": "男", "ethnicity": "蒙古族", "birth": "1982-08", "birthplace": "待查",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委副书记、市长", "current_org": "阿尔山市人民政府",
     "source": "http://www.aes.gov.cn/aes/2024-12/18/article_2024121816263138199.html"},
    # ---- 现任市委常委/副市长 ----
    {"id": 3, "name": "徐英姝", "gender": "女", "ethnicity": "汉族", "birth": "1987-03", "birthplace": "待查",
     "education": "法学硕士", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委常委、常务副市长", "current_org": "阿尔山市人民政府",
     "source": "http://www.aes.gov.cn/aes/2023-03/30/article_2023121701273240574.html"},
    {"id": 4, "name": "邰海峰", "gender": "男", "ethnicity": "蒙古族", "birth": "1981-12", "birthplace": "待查",
     "education": "内蒙古大学公共管理硕士", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委常委、副市长", "current_org": "阿尔山市人民政府",
     "source": "http://www.aes.gov.cn/aes/2024-12/18/article_2024121816193233196.html"},
    {"id": 5, "name": "李梁", "gender": "男", "ethnicity": "汉族", "birth": "1980-07", "birthplace": "待查",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委常委、副市长(京蒙协作)", "current_org": "阿尔山市人民政府",
     "source": "http://www.aes.gov.cn/aes/2025-09/23/article_2025092315073263524.html"},
    {"id": 6, "name": "张国栋", "gender": "男", "ethnicity": "汉族", "birth": "1988-05", "birthplace": "待查",
     "education": "大学学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委常委、副市长(挂职,文化和旅游部定点帮扶)", "current_org": "阿尔山市人民政府",
     "source": "http://www.aes.gov.cn/aes/2026-07/15/article_2026071515592592650.html"},
    {"id": 7, "name": "刘志强", "gender": "男", "ethnicity": "汉族", "birth": "1975-06", "birthplace": "待查",
     "education": "大学学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "副市长、公安局党委书记局长", "current_org": "阿尔山市人民政府",
     "source": "http://www.aes.gov.cn/aes/2022-01/05/article_2023121701273278082.html"},
    {"id": 8, "name": "李鹏", "gender": "男", "ethnicity": "汉族", "birth": "1986-06", "birthplace": "待查",
     "education": "硕士研究生", "party_join": "中共党员", "work_start": "待查",
     "current_post": "副市长(旅游/文体/市场)", "current_org": "阿尔山市人民政府",
     "source": "http://www.aes.gov.cn/aes/2025-02/11/article_2025021111113428658.html"},
    {"id": 9, "name": "国庆", "gender": "男", "ethnicity": "蒙古族", "birth": "1981-10", "birthplace": "待查",
     "education": "大学本科", "party_join": "中共党员", "work_start": "待查",
     "current_post": "副市长(民族/交通/农牧/水利/林草/乡村振兴)", "current_org": "阿尔山市人民政府",
     "source": "http://www.aes.gov.cn/aes/2026-07/15/article_2026071515205836136.html"},
    {"id": 10, "name": "韩涛", "gender": "男", "ethnicity": "汉族", "birth": "1986-05", "birthplace": "待查",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "副市长(外事口岸/商务/卫健/招商)", "current_org": "阿尔山市人民政府",
     "source": "http://www.aes.gov.cn/aes/2026-07/15/article_2026071515422532033.html"},
    # ---- 党纪/监委 ----
    {"id": 11, "name": "王磊", "gender": "待查", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市监察委员会代主任", "current_org": "阿尔山市监察委员会",
     "source": "http://www.aes.gov.cn/aes/2026-07/23/article_2026072315594643363.html"},
    # ---- 人大 / 政协 ----
    {"id": 12, "name": "赵德权", "gender": "待查", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市人大常委会党组书记、主任", "current_org": "阿尔山市人大常委会",
     "source": "http://www.aes.gov.cn/aes/2024-01/20/article_2024041410303xxxxxx.html"},
    {"id": 13, "name": "张志军", "gender": "待查", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市政协党组书记、主席", "current_org": "政协阿尔山市委员会",
     "source": "http://www.aes.gov.cn/aes/2024-01/20/article_2024041410303xxxxxx.html"},
    # ---- 前任主官 ----
    {"id": 14, "name": "杨永久", "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "兴安盟人大工委副主任", "current_org": "兴安盟人大工委",
     "source": "http://www.aes.gov.cn/aes/2026-06/30/article_2026063009121443663.html"},
    {"id": 15, "name": "王晓欢", "gender": "待查", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "待查", "current_org": "待查",
     "source": "http://www.aes.gov.cn/aes/2022-01/24/article_2023121701293464151.html"},
    {"id": 16, "name": "李贺", "gender": "待查", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "待查", "current_org": "待查",
     "source": "http://www.aes.gov.cn/aes/2020-01/01/article_2023121701293433699.html"},
]

# ---------------------------------------------------------------------------
# organizations
# ---------------------------------------------------------------------------
organizations = [
    {"id": 1, "name": "中共阿尔山市委员会", "type": "党委", "level": "县级", "parent": "中共兴安盟委员会", "location": "内蒙古自治区兴安盟阿尔山市"},
    {"id": 2, "name": "阿尔山市人民政府", "type": "政府", "level": "县级", "parent": "兴安盟行政公署", "location": "内蒙古自治区兴安盟阿尔山市"},
    {"id": 3, "name": "阿尔山市监察委员会", "type": "纪委", "level": "县级", "parent": "内蒙古自治区监察委员会", "location": "内蒙古自治区兴安盟阿尔山市"},
    {"id": 4, "name": "阿尔山市人大常委会", "type": "人大", "level": "县级", "parent": "兴安盟人大工作委员会", "location": "内蒙古自治区兴安盟阿尔山市"},
    {"id": 5, "name": "政协阿尔山市委员会", "type": "政协", "level": "县级", "parent": "政协兴安盟委员会", "location": "内蒙古自治区兴安盟阿尔山市"},
    {"id": 6, "name": "中共兴安盟委员会", "type": "党委", "level": "地级", "parent": "中共内蒙古自治区委员会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 7, "name": "兴安盟行政公署", "type": "政府", "level": "地级", "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 8, "name": "兴安盟人大工作委员会", "type": "人大", "level": "地级", "parent": "内蒙古自治区人大常委会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
]

# ---------------------------------------------------------------------------
# positions
# ---------------------------------------------------------------------------
positions = [
    # 现任党委
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "约2026年7月接替杨永久(交接时间待核)"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持市政府全面工作，负责审计监督"},
    # 现任市委常委
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责市政府常务工作，分管发改/财政/应急"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管住建/生态环境/自然资源/城管"},
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助市长负责京蒙协作等方面工作"},
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "挂职"},
    {"person_id": 6, "org_id": 2, "title": "副市长(挂职)", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "文化和旅游部定点帮扶"},
    # 现任副市长
    {"person_id": 7, "org_id": 2, "title": "副市长、市公安局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "公安/司法/信访/国安"},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "旅游开发/文体/市场管理/论坛会议"},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "民族/交通/农牧/水利/林草/乡村振兴"},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "外事口岸/商务/卫生健康/招商"},
    # 党纪
    {"person_id": 11, "org_id": 3, "title": "市监委代主任", "start_date": "2026-07-16", "end_date": "present", "rank": "副处级", "note": "七届人大常委会第二十九次会议决定"},
    # 人大/政协
    {"person_id": 12, "org_id": 4, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "市人大常委会党组书记、主任"},
    {"person_id": 13, "org_id": 5, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "市政协党组书记、主席"},
    # 前任
    {"person_id": 14, "org_id": 1, "title": "市委书记(原)", "start_date": "", "end_date": "2026-07", "rank": "正处级", "note": "盟人大工委副主任兼阿尔山市委书记，约2026年7月交班给耿浩"},
    {"person_id": 14, "org_id": 8, "title": "盟人大工委副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "市长(原)", "start_date": "2021", "end_date": "", "rank": "正处级", "note": "2021任市委副书记、代市长，后市长"},
    {"person_id": 16, "org_id": 2, "title": "市长(原)", "start_date": "", "end_date": "2021", "rank": "正处级", "note": "2019年时任阿尔山市委副书记、市长"},
]

# ---------------------------------------------------------------------------
# relationships
# ---------------------------------------------------------------------------
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "市委书记-市长党政正职搭档，新任书记与搭档协同推进文旅兴市", "overlap_org": "中共阿尔山市委员会", "overlap_period": "2026—present"},
    {"person_a": 14, "person_b": 1, "type": "前后任", "context": "杨永久任盟人大工委副主任兼阿尔山市委书记，约2026-07移交耿浩", "overlap_org": "中共阿尔山市委员会", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "额日赫木图为市委副书记、市长，杨永久任市委书记时为其上级(2026上半年)", "overlap_org": "中共阿尔山市委员会", "overlap_period": "2024-2026-07"},
    {"person_a": 2, "person_b": 15, "type": "前后任", "context": "王晓欢任前市长(约2021-?)，由额日赫木图接任", "overlap_org": "阿尔山市人民政府", "overlap_period": ""},
    {"person_a": 16, "person_b": 15, "type": "前后任", "context": "李贺任市长(2019)，后由王晓欢接任", "overlap_org": "阿尔山市人民政府", "overlap_period": "2019-2021"},
    {"person_a": 2, "person_b": 3, "type": "AB角", "context": "市长-常务副市长正副手配对(徐英瑛负责政府常务)", "overlap_org": "阿尔山市人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 2, "type": "上下级", "context": "李梁协助市长负责京蒙协作", "overlap_org": "阿尔山市人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 2, "type": "上下级", "context": "张国栋挂职副市长，协助文旅部定点帮扶共建", "overlap_org": "阿尔山市人民政府", "overlap_period": "2026-07—present"},
    {"person_a": 1, "person_b": 12, "type": "同僚", "context": "市人大主任赵德权陪同耿浩调研市人大机关", "overlap_org": "中共阿尔山市委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 13, "type": "同僚", "context": "市政协主席张志军陪同耿浩调研市政协机关", "overlap_org": "中共阿尔山市委员会", "overlap_period": "2026-07"},
    {"person_a": 11, "person_b": 1, "type": "上下级", "context": "耿浩(市委书记)赴市纪委监委调研，王磊(监委代主任)为下级", "overlap_org": "阿尔山市监察委员会", "overlap_period": "2026-07"},
]

if __name__ == "__main__":
    run_build(
        slug=slug,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )
    print(f"Done! DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")