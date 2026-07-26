#!/usr/bin/env python3
"""Build 孝义市 leadership network database and GEXF graph.

Current leadership as of 2026-07-26 (confirmed from official government website):

市委书记: 刘世庆
  - Born 1970.10, 离石师范学校中专毕业、中央党校函授学院法律专业本科毕业
  - Also 吕梁市人大常委会副主任 (concurrently)
  - Source: xiaoyi.gov.cn official leadership page

市委副书记、市长: 郭清智
  - Born 1982.04, 山西汾阳人, 农业推广硕士, 大学学历
  - 2004.12 joined CPC, 2003.11 started work
  - Source: Baidu Baike

Full leadership roster confirmed from:
  http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/

Research limitations (2026-07-26):
- 刘世庆's complete career timeline (pre-2021) needs further research
- Some deputy career timelines are incomplete
- Specific relationship evidence is primarily inferred from organizational overlap
"""

from pathlib import Path
import sqlite3
import sys

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

STAGING_DIR = Path(__file__).parent
DB_PATH = STAGING_DIR / "孝义市_network.db"
GEXF_PATH = STAGING_DIR / "孝义市_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    {
        "id": 1,
        "name": "刘世庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970.10",
        "birthplace": "山西省吕梁市",
        "education": "离石师范学校中专、中央党校函授学院法律专业本科",
        "party_join": "",
        "work_start": "",
        "current_post": "吕梁市人大常委会副主任、孝义市委书记",
        "current_org": "中共孝义市委员会",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 2,
        "name": "郭清智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982.04",
        "birthplace": "山西省吕梁市汾阳市",
        "education": "山西农业大学农林经济管理本科、农业推广硕士",
        "party_join": "2004.12",
        "work_start": "2003.11",
        "current_post": "孝义市委副书记、市长",
        "current_org": "孝义市人民政府",
        "source": "https://baike.baidu.com/item/%E9%83%AD%E6%B8%85%E6%99%BA",
    },
    {
        "id": 3,
        "name": "崔宇飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市委副书记",
        "current_org": "中共孝义市委员会",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 4,
        "name": "肖近三",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市委常委、纪委书记、监委主任",
        "current_org": "中共孝义市纪律检查委员会",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 5,
        "name": "李玉昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市委常委、组织部部长",
        "current_org": "中共孝义市委员会",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 6,
        "name": "吕晓全",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市委常委、政法委书记",
        "current_org": "中共孝义市委员会",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 7,
        "name": "张耀东",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市委常委、统战部部长",
        "current_org": "中共孝义市委员会",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 8,
        "name": "史东山",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市委常委、副市长",
        "current_org": "孝义市人民政府",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 9,
        "name": "白志刚",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市委常委、人武部上校政治委员",
        "current_org": "孝义市人民武装部",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 10,
        "name": "王潇潇",
        "gender": "女",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市委常委、宣传部部长",
        "current_org": "中共孝义市委员会",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 11,
        "name": "薛鹏燕",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市委常委、副市长",
        "current_org": "孝义市人民政府",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 12,
        "name": "王颢",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市副市长、市公安局局长",
        "current_org": "孝义市人民政府",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 13,
        "name": "杨凤鸣",
        "gender": "女",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市副市长",
        "current_org": "孝义市人民政府",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 14,
        "name": "薛志强",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市副市长",
        "current_org": "孝义市人民政府",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 15,
        "name": "任小俊",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市副市长",
        "current_org": "孝义市人民政府",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
    {
        "id": 16,
        "name": "续晓强",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝义市副市长",
        "current_org": "孝义市人民政府",
        "source": "http://www.xiaoyi.gov.cn/xxgk/fdzdgknr/ldxx/",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共孝义市委员会",
        "type": "党委",
        "level": "县级",
        "location": "孝义市",
    },
    {
        "id": 2,
        "name": "孝义市人民政府",
        "type": "政府",
        "level": "县级",
        "location": "孝义市",
    },
    {
        "id": 3,
        "name": "中共孝义市纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "location": "孝义市",
    },
    {
        "id": 4,
        "name": "孝义市人民武装部",
        "type": "事业单位",
        "level": "县级",
        "location": "孝义市",
    },
    {
        "id": 5,
        "name": "吕梁市人大常委会",
        "type": "人大",
        "level": "地市级",
        "location": "吕梁市",
    },
    {
        "id": 6,
        "name": "孝义市公安局",
        "type": "政府",
        "level": "县级",
        "location": "孝义市",
    },
    {
        "id": 7,
        "name": "汾阳市峪道河镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "location": "汾阳市",
    },
    {
        "id": 8,
        "name": "汾阳市阳城乡",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "location": "汾阳市",
    },
    {
        "id": 9,
        "name": "汾阳市栗家庄乡",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "location": "汾阳市",
    },
    {
        "id": 10,
        "name": "共青团吕梁市委",
        "type": "群团",
        "level": "地市级",
        "location": "吕梁市",
    },
    {
        "id": 11,
        "name": "吕梁市民政局",
        "type": "政府",
        "level": "地市级",
        "location": "吕梁市",
    },
    {
        "id": 12,
        "name": "中共柳林县委员会",
        "type": "党委",
        "level": "县级",
        "location": "柳林县",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════════

positions = [
    # 刘世庆 (id=1) - 市委书记
    {"person_id": 1, "org_id": 1, "title": "孝义市委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "现任孝义市委书记"},
    {"person_id": 1, "org_id": 5, "title": "吕梁市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任吕梁市人大常委会副主任"},
    # 刘世庆 earlier career needs research - gaps exist before 2018

    # 郭清智 (id=2) - 市长 (full timeline from Baidu Baike)
    {"person_id": 2, "org_id": 2, "title": "孝义市委副书记、市长", "start_date": "2021.12", "end_date": "", "rank": "正县级", "note": "2021.12 孝义市人大补选为市长"},
    {"person_id": 2, "org_id": 7, "title": "汾阳市峪道河镇副镇长", "start_date": "2003.11", "end_date": "2007.04", "rank": "副科级", "note": "工作起点"},
    {"person_id": 2, "org_id": 8, "title": "汾阳市阳城乡政协联络组组长", "start_date": "2007.04", "end_date": "2010.08", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "汾阳市栗家庄乡党委书记", "start_date": "2010.08", "end_date": "2011.04", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "汾阳市栗家庄乡党委书记、人大主席", "start_date": "2011.04", "end_date": "2012.10", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "共青团吕梁市委副书记、党组成员", "start_date": "2012.10", "end_date": "2016.12", "rank": "副县级", "note": "2013.02-2014.02挂职团中央农村青年工作部农村发展处副处长"},
    {"person_id": 2, "org_id": 10, "title": "共青团吕梁市委书记、党组书记", "start_date": "2016.12", "end_date": "2019.07", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "吕梁市民政局党组书记", "start_date": "2019.07", "end_date": "2019.08", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "吕梁市民政局局长、党组书记", "start_date": "2019.08", "end_date": "2021.03", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "柳林县委副书记、党校校长", "start_date": "2021.03", "end_date": "2021.12", "rank": "副县级", "note": ""},

    # 崔宇飞 (id=3) - 副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任孝义市委副书记"},

    # 肖近三 (id=4) - 纪委书记
    {"person_id": 4, "org_id": 3, "title": "市委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},

    # 李玉昌 (id=5) - 组织部长
    {"person_id": 5, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},

    # 吕晓全 (id=6) - 政法委书记
    {"person_id": 6, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},

    # 张耀东 (id=7) - 统战部长
    {"person_id": 7, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},

    # 史东山 (id=8) - 常委副市长
    {"person_id": 8, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},

    # 白志刚 (id=9) - 人武部政委
    {"person_id": 9, "org_id": 4, "title": "市委常委、人武部上校政治委员", "start_date": "", "end_date": "", "rank": "上校", "note": "现任"},

    # 王潇潇 (id=10) - 宣传部长
    {"person_id": 10, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},

    # 薛鹏燕 (id=11) - 常委副市长
    {"person_id": 11, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},

    # 王颢 (id=12) - 副市长/公安局长
    {"person_id": 12, "org_id": 2, "title": "副市长、市公安局局长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 12, "org_id": 6, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "副县级", "note": "兼任"},

    # 杨凤鸣 (id=13) - 副市长
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},

    # 薛志强 (id=14) - 副市长
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},

    # 任小俊 (id=15) - 副市长
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},

    # 续晓强 (id=16) - 副市长
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "刘世庆（市委书记）与郭清智（市长）为孝义市现任党政正职",
        "overlap_org": "孝义市",
        "overlap_period": "2021.12-至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "班子共事",
        "context": "刘世庆与崔宇飞在孝义市委班子共事",
        "overlap_org": "中共孝义市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "班子共事",
        "context": "刘世庆与肖近三在市委班子共事（党政正职+纪委书记）",
        "overlap_org": "中共孝义市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "班子共事",
        "context": "刘世庆与李玉昌在市委班子共事（党政正职+组织部长）",
        "overlap_org": "中共孝义市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "班子共事",
        "context": "刘世庆与史东山在市委常委班子共事",
        "overlap_org": "中共孝义市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 11,
        "type": "班子共事",
        "context": "刘世庆与薛鹏燕在市委常委班子共事",
        "overlap_org": "中共孝义市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "上下级",
        "context": "郭清智(市长)与史东山(常委副市长)在政府班子共事",
        "overlap_org": "孝义市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 11,
        "type": "上下级",
        "context": "郭清智(市长)与薛鹏燕(常委副市长)在政府班子共事",
        "overlap_org": "孝义市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "上下级",
        "context": "郭清智(市长)与王颢(副市长、公安局长)在政府班子共事",
        "overlap_org": "孝义市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "上下级",
        "context": "郭清智(市长)与杨凤鸣(副市长)在政府班子共事",
        "overlap_org": "孝义市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 14,
        "type": "上下级",
        "context": "郭清智(市长)与薛志强(副市长)在政府班子共事",
        "overlap_org": "孝义市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 15,
        "type": "上下级",
        "context": "郭清智(市长)与任小俊(副市长)在政府班子共事",
        "overlap_org": "孝义市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 16,
        "type": "上下级",
        "context": "郭清智(市长)与续晓强(副市长)在政府班子共事",
        "overlap_org": "孝义市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "班子共事",
        "context": "崔宇飞与肖近三在市委班子共事",
        "overlap_org": "中共孝义市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 5,
        "person_b": 7,
        "type": "班子共事",
        "context": "李玉昌与张耀东分别为组织部长和统战部长，在市委班子共事",
        "overlap_org": "中共孝义市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 10,
        "person_b": 1,
        "type": "上下级",
        "context": "王潇潇(宣传部长)在刘世庆(市委书记)领导下工作",
        "overlap_org": "中共孝义市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 8,
        "person_b": 11,
        "type": "班子共事",
        "context": "史东山与薛鹏燕均为市委常委、副市长",
        "overlap_org": "孝义市人民政府",
        "overlap_period": "至今",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="孝义市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )