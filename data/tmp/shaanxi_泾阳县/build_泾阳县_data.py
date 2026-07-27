#!/usr/bin/env python3
"""Build script for 泾阳县 (Jingyang County, 咸阳市, 陕西省) government personnel network.

Data sources:
- 泾阳县政府领导之窗: https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/
- 泾阳县政府新闻: https://www.snjingyang.gov.cn/xwzx/zwyw/
- 咸阳市人民政府: https://www.xianyang.gov.cn/

Research date: 2026-07-25
"""

import sqlite3
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
STAGING = Path(__file__).parent
DB_PATH = STAGING / "泾阳县_network.db"
GEXF_PATH = STAGING / "泾阳县_network.gexf"

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

persons = [
    # --- 县委 (County Party Committee) ---
    {
        "id": 1,
        "name": "郝瑞耀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共泾阳县委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xw/hry/",
    },
    {
        "id": 2,
        "name": "王洲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "",
        "native_place": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "泾阳县人民政府",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xw/wz/",
    },
    {
        "id": 3,
        "name": "刘战军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年9月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共泾阳县委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xw/lzj/",
    },
    {
        "id": 4,
        "name": "康宇麟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年8月",
        "birthplace": "",
        "native_place": "",
        "education": "经济学硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共泾阳县委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xw/kyl/",
    },
    {
        "id": 5,
        "name": "谭会党",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年6月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记，县监察委员会主任",
        "current_org": "中共泾阳县纪律检查委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xw/thd/",
    },
    {
        "id": 6,
        "name": "贾晓妮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共泾阳县委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xw/jxn/",
    },
    {
        "id": 7,
        "name": "杨利荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年6月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "泾阳县人民政府",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xw/ylr/",
    },
    {
        "id": 8,
        "name": "高明博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "泾阳县人民政府",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xw/lr/",
    },
    {
        "id": 9,
        "name": "陈新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年7月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历、博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共泾阳县委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xw/sx/",
    },
    # --- 县人大 (People's Congress) ---
    {
        "id": 10,
        "name": "张宣朝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "陕西兴平",
        "native_place": "陕西兴平",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "泾阳县人民代表大会常务委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xrd/zxc/",
    },
    {
        "id": 11,
        "name": "吴李兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年12月",
        "birthplace": "陕西泾阳",
        "native_place": "陕西泾阳",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "泾阳县人民代表大会常务委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xrd/wlb/",
    },
    {
        "id": 12,
        "name": "余西英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年9月",
        "birthplace": "陕西三原",
        "native_place": "陕西三原",
        "education": "大学学历",
        "party_join": "无党派",
        "work_start": "1997年7月",
        "current_post": "县人大常委会副主任",
        "current_org": "泾阳县人民代表大会常务委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xrd/yxy/",
    },
    {
        "id": 13,
        "name": "王东京",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年2月",
        "birthplace": "陕西泾阳",
        "native_place": "陕西泾阳",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "泾阳县人民代表大会常务委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xrd/wdj/",
    },
    # --- 县政府 (County Government) ---
    {
        "id": 14,
        "name": "邹国行",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泾阳县人民政府",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xzf/zgx/",
    },
    {
        "id": 15,
        "name": "杨熠书",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985年2月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泾阳县人民政府",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xzf/yys/",
    },
    {
        "id": 16,
        "name": "张速成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "泾阳县人民政府",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xzf/sz/",
    },
    {
        "id": 17,
        "name": "程峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泾阳县人民政府",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xzf/cf/",
    },
    {
        "id": 18,
        "name": "邓涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年3月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泾阳县人民政府",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xzf/dt/",
    },
    # --- 县政协 (Political Consultative Conference) ---
    {
        "id": 19,
        "name": "刘海燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967年10月",
        "birthplace": "",
        "native_place": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "1984年12月",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议泾阳县委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xzx/lhy/",
    },
    {
        "id": 20,
        "name": "陈涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年8月",
        "birthplace": "陕西泾阳",
        "native_place": "陕西泾阳",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "1989年7月",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议泾阳县委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xzx/ct/",
    },
    {
        "id": 21,
        "name": "杨永良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "陕西泾阳",
        "native_place": "陕西泾阳",
        "education": "本科",
        "party_join": "",
        "work_start": "1993年7月",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议泾阳县委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xzx/yyl/",
    },
    {
        "id": 22,
        "name": "党振林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "陕西泾阳",
        "native_place": "陕西泾阳",
        "education": "研究生",
        "party_join": "中国农工民主党",
        "work_start": "1996年9月",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议泾阳县委员会",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xzx/dzl/",
    },
    # --- 两院 (Court and Procuratorate) ---
    {
        "id": 23,
        "name": "高继超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年7月",
        "birthplace": "",
        "native_place": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泾阳县人民法院党组书记、院长",
        "current_org": "泾阳县人民法院",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xfy/gjc/",
    },
    {
        "id": 24,
        "name": "张雅茹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967年11月",
        "birthplace": "陕西周至",
        "native_place": "陕西周至",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1991年8月",
        "current_post": "泾阳县人民检察院党组书记、检察长",
        "current_org": "泾阳县人民检察院",
        "source": "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xjcy/zyr/",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共泾阳县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共咸阳市委员会",
        "location": "陕西省咸阳市泾阳县",
    },
    {
        "id": 2,
        "name": "泾阳县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "咸阳市人民政府",
        "location": "陕西省咸阳市泾阳县",
    },
    {
        "id": 3,
        "name": "中共泾阳县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共泾阳县委员会",
        "location": "陕西省咸阳市泾阳县",
    },
    {
        "id": 4,
        "name": "泾阳县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "",
        "location": "陕西省咸阳市泾阳县",
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议泾阳县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "",
        "location": "陕西省咸阳市泾阳县",
    },
    {
        "id": 6,
        "name": "泾阳县人民法院",
        "type": "事业单位",
        "level": "县级",
        "parent": "",
        "location": "陕西省咸阳市泾阳县",
    },
    {
        "id": 7,
        "name": "泾阳县人民检察院",
        "type": "事业单位",
        "level": "县级",
        "parent": "",
        "location": "陕西省咸阳市泾阳县",
    },
]

positions = [
    # 郝瑞耀 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "未知（2026年前后）", "end": "至今", "rank": "正处级", "note": "曾任泾阳县委副书记、县长后晋升"},
    # 王洲 - 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "未知", "end": "至今", "rank": "正处级", "note": "曾任咸阳市生态环境局党组书记、局长"},
    # 刘战军 - 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "未知", "end": "至今", "rank": "副处级", "note": "曾任泾阳县委常委、常务副县长"},
    # 康宇麟 - 宣传部部长
    {"person_id": 4, "org_id": 1, "title": "县委常委、宣传部部长", "start": "未知", "end": "至今", "rank": "副处级", "note": "曾任兴平市副市长、西城街道党工委书记（兼）"},
    # 谭会党 - 纪委书记
    {"person_id": 5, "org_id": 3, "title": "县委常委、县纪委书记、县监委主任", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    # 贾晓妮 - 政法委书记
    {"person_id": 6, "org_id": 1, "title": "县委常委、政法委书记", "start": "未知", "end": "至今", "rank": "副处级", "note": "曾任泾阳县政府党组成员、副县长"},
    # 杨利荣 - 副县长
    {"person_id": 7, "org_id": 2, "title": "县委常委、副县长", "start": "未知", "end": "至今", "rank": "副处级", "note": "曾任泾阳县委常委、统战部部长"},
    # 高明博 - 常务副县长
    {"person_id": 8, "org_id": 2, "title": "县委常委、常务副县长", "start": "未知", "end": "至今", "rank": "副处级", "note": "曾任武功县委常委、副县长"},
    # 陈新 - 组织部部长
    {"person_id": 9, "org_id": 1, "title": "县委常委、组织部部长", "start": "未知", "end": "至今", "rank": "副处级", "note": "曾任咸阳市高新区党工委委员、管委会副主任"},
    # 张宣朝 - 人大主任
    {"person_id": 10, "org_id": 4, "title": "县人大常委会主任", "start": "未知", "end": "至今", "rank": "正处级", "note": "曾任泾阳县委常委、宣传部部长"},
    # 吴李兵 - 人大副主任
    {"person_id": 11, "org_id": 4, "title": "县人大常委会副主任", "start": "未知", "end": "至今", "rank": "副处级", "note": "陕西泾阳人，曾任云阳镇党委书记、县审计局局长"},
    # 余西英 - 人大副主任
    {"person_id": 12, "org_id": 4, "title": "县人大常委会副主任", "start": "未知", "end": "至今", "rank": "副处级", "note": "陕西三原人，无党派，曾任泾阳县政协副主席"},
    # 王东京 - 人大副主任
    {"person_id": 13, "org_id": 4, "title": "县人大常委会副主任", "start": "未知", "end": "至今", "rank": "副处级", "note": "陕西泾阳人，曾任泾阳县纪委副书记、监委副主任"},
    # 邹国行 - 副县长
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "未知", "end": "至今", "rank": "副处级", "note": "民盟盟员，曾任长武县副县长"},
    # 杨熠书 - 副县长
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "未知", "end": "至今", "rank": "副处级", "note": "曾任共青团咸阳市委副书记"},
    # 张速成 - 副县长、公安局长
    {"person_id": 16, "org_id": 2, "title": "副县长、县公安局局长", "start": "未知", "end": "至今", "rank": "副处级", "note": "曾任礼泉县公安局政委"},
    # 程峰 - 副县长
    {"person_id": 17, "org_id": 2, "title": "副县长", "start": "未知", "end": "至今", "rank": "副处级", "note": "曾任旬邑县交通运输局局长"},
    # 邓涛 - 副县长
    {"person_id": 18, "org_id": 2, "title": "副县长", "start": "未知", "end": "至今", "rank": "副处级", "note": "曾任泾阳县委办公室主任"},
    # 刘海燕 - 政协主席
    {"person_id": 19, "org_id": 5, "title": "县政协主席", "start": "未知", "end": "至今", "rank": "正处级", "note": "曾任兴平市委常委、宣传部部长"},
    # 陈涛 - 政协副主席
    {"person_id": 20, "org_id": 5, "title": "县政协副主席", "start": "未知", "end": "至今", "rank": "副处级", "note": "陕西泾阳人，曾任泾阳县人社局局长"},
    # 杨永良 - 政协副主席
    {"person_id": 21, "org_id": 5, "title": "县政协副主席", "start": "未知", "end": "至今", "rank": "副处级", "note": "陕西泾阳人"},
    # 党振林 - 政协副主席
    {"person_id": 22, "org_id": 5, "title": "县政协副主席", "start": "未知", "end": "至今", "rank": "副处级", "note": "陕西泾阳人，农工党党员"},
    # 高继超 - 法院院长
    {"person_id": 23, "org_id": 6, "title": "党组书记、院长", "start": "未知", "end": "至今", "rank": "副处级", "note": "曾任咸阳市中级人民法院办公室主任"},
    # 张雅茹 - 检察院检察长
    {"person_id": 24, "org_id": 7, "title": "党组书记、检察长", "start": "未知", "end": "至今", "rank": "副处级（三级高级检察官）", "note": "曾任淳化县人民检察院检察长"},
]

relationships = [
    # Work overlap relationships in the county committee
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "郝瑞耀（县委书记）与王洲（县长）为党政主要领导搭档", "overlap_org": "中共泾阳县委员会/泾阳县人民政府", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "郝瑞耀（县委书记）与刘战军（县委副书记）在县委常委会共事", "overlap_org": "中共泾阳县委员会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "郝瑞耀（县委书记）与高明博（常务副县长）在县委、县政府共事", "overlap_org": "中共泾阳县委员会", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "王洲（县长）与高明博（常务副县长）在县政府搭档", "overlap_org": "泾阳县人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "王洲（县长）与杨利荣（县委常委、副县长）在县政府搭档", "overlap_org": "泾阳县人民政府", "overlap_period": "2026年"},
    {"person_a": 9, "person_b": 1, "type": "superior_subordinate", "context": "陈新（组织部部长）在县委常委会受郝瑞耀（县委书记）领导", "overlap_org": "中共泾阳县委员会", "overlap_period": "2026年"},
    # Same institution / system connections
    {"person_a": 5, "person_b": 1, "type": "superior_subordinate", "context": "谭会党（纪委书记）在县委常委会受郝瑞耀领导", "overlap_org": "中共泾阳县委员会", "overlap_period": "2026年"},
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate", "context": "贾晓妮（政法委书记）在县委常委会受郝瑞耀领导", "overlap_org": "中共泾阳县委员会", "overlap_period": "2026年"},
    {"person_a": 4, "person_b": 1, "type": "superior_subordinate", "context": "康宇麟（宣传部部长）在县委常委会受郝瑞耀领导", "overlap_org": "中共泾阳县委员会", "overlap_period": "2026年"},
    # Predecessor-successor (郝瑞耀 was previously 县长, now 县委书记)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "郝瑞耀此前担任泾阳县县长，晋升县委书记后；王洲接任县长", "overlap_org": "泾阳县人民政府", "overlap_period": "2025-2026年（推测交接期）"},
    # 贾晓妮 - was previously 副县长, now 政法委书记
    {"person_a": 6, "person_b": 2, "type": "superior_subordinate", "context": "贾晓妮（政法委书记）此前曾任副县长，在县政府与王洲共事", "overlap_org": "泾阳县人民政府", "overlap_period": "此前"},
    # 张宣朝 - rotated from 宣传部部长 to 人大主任
    {"person_a": 10, "person_b": 1, "type": "overlap", "context": "张宣朝（人大主任）曾任泾阳县委常委、宣传部部长，在县委常委会与郝瑞耀共事", "overlap_org": "中共泾阳县委员会", "overlap_period": "此前"},
    # 高明博 - 武功县交流到泾阳
    {"person_a": 8, "person_b": 2, "type": "superior_subordinate", "context": "高明博（常务副县长）从武功县交流至泾阳，与王洲在县政府搭档", "overlap_org": "泾阳县人民政府", "overlap_period": "2026年"},
    # 同级班子成员交叉
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "杨利荣（县委常委、副县长）与高明博（县委常委、常务副县长）同为县委常委、县政府领导", "overlap_org": "中共泾阳县委员会/泾阳县人民政府", "overlap_period": "2026年"},
    {"person_a": 14, "person_b": 17, "type": "overlap", "context": "邹国行（副县长）与程峰（副县长）同为县政府领导班子成员", "overlap_org": "泾阳县人民政府", "overlap_period": "2026年"},
    # 本地干部（泾阳籍）
    {"person_a": 11, "person_b": 13, "type": "overlap", "context": "吴李兵（人大副主任，泾阳籍）与王东京（人大副主任，泾阳籍）同为泾阳籍县领导", "overlap_org": "泾阳县人民代表大会常务委员会", "overlap_period": "2026年"},
    # 两院
    {"person_a": 23, "person_b": 1, "type": "superior_subordinate", "context": "高继超（法院院长）受县委领导", "overlap_org": "中共泾阳县委员会", "overlap_period": "2026年"},
    {"person_a": 24, "person_b": 1, "type": "superior_subordinate", "context": "张雅茹（检察院检察长）受县委领导", "overlap_org": "中共泾阳县委员会", "overlap_period": "2026年"},
]


# ---------------------------------------------------------------------------
# Build SQLite DB
# ---------------------------------------------------------------------------
def build_db():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")

    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start_date TEXT,
            end_date TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert data
    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p.get("birthplace", ""),
             p["education"], p["party_join"], p.get("work_start", ""),
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions
            (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")


# ---------------------------------------------------------------------------
# Build GEXF
# ---------------------------------------------------------------------------
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "县委" in post and "纪委" not in post:
        return "255,50,50"  # Red - party secretary
    elif "县长" in post or "副县长" in post or "区长" in post:
        return "50,100,255"  # Blue - government
    elif "纪委" in post or "监察" in post:
        return "255,165,0"  # Orange - discipline
    elif "人大" in post:
        return "200,255,255"  # Cyan - people's congress
    elif "政协" in post:
        return "255,240,200"  # Cream - political consultative
    elif "法院" in post or "检察" in post:
        return "200,200,255"  # Light blue - judiciary
    else:
        return "100,100,100"  # Grey - other


def org_color(o):
    t = o.get("type", "")
    if t == "党委":
        return "255,200,200"  # Pink
    elif t == "政府":
        return "200,200,255"  # Light blue
    elif t == "人大":
        return "200,255,255"  # Cyan
    elif t == "政协":
        return "255,240,200"  # Cream
    elif t == "事业单位":
        return "220,220,220"  # Light grey
    else:
        return "200,200,200"


def is_top_leader(p):
    post = p.get("current_post", "")
    return ("县委书记" in post and "纪委" not in post) or ("县长" in post and "副" not in post) or ("人大主任" in post) or ("政协主席" in post)


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>泾阳县领导班子工作关系网络 - 陕西省咸阳市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        attrs = [
            f'          <attvalue for="0" value="person"/>',
            f'          <attvalue for="1" value="{esc(p["current_post"])}"/>',
            f'          <attvalue for="2" value="{esc(p["current_org"])}"/>',
        ]
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.extend(attrs)
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges: Positions (person -> organization)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: Relationships (person <-> person)
    for r in relationships:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
def print_summary():
    print(f"\n{'='*60}")
    print(f"泾阳县 Personnel Network Build Summary")
    print(f"{'='*60}")
    print(f"Persons:       {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions:     {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"DB:            {DB_PATH}")
    print(f"GEXF:          {GEXF_PATH}")
    print(f"{'='*60}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
