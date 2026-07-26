#!/usr/bin/env python3
"""Build 万荣县 (Wanrong County) personnel network database + GEXF graph.

Targets: 县委书记 (王飞), 县长 (仪天亮)
Data sources:
- 万荣县政府官网领导之窗 (https://www.wanrong.gov.cn/zfxxgk/fdzdgknr/ldzc/)
  -- 县委领导: https://www.wanrong.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/index.shtml
  -- 县政府领导: https://www.wanrong.gov.cn/zfxxgk/fdzdgknr/ldzc/xzfld/index.shtml
  -- 县人大领导: https://www.wanrong.gov.cn/zfxxgk/fdzdgknr/ldzc/xrdld/index.shtml
  -- 县政协领导: https://www.wanrong.gov.cn/zfxxgk/fdzdgknr/ldzc/xzxld/index.shtml
  -- 县长副县长分工: https://www.wanrong.gov.cn/doc/2026/05/06/604826.shtml
"""

import sqlite3
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) == 'shanxi_万荣县':
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..'))
else:
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

DB_PATH = os.path.join(PROJECT_ROOT, "data/database/万荣县_network.db")
GEXF_PATH = os.path.join(PROJECT_ROOT, "data/graph/万荣县_network.gexf")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

# ========== OFFICIAL SOURCE URLS ==========
LDZC_ROOT = "https://www.wanrong.gov.cn/zfxxgk/fdzdgknr/ldzc"
URL_XWLD = LDZC_ROOT + "/xwld/index.shtml"
URL_XZFLD = LDZC_ROOT + "/xzfld/index.shtml"
URL_XRDLD = LDZC_ROOT + "/xrdld/index.shtml"
URL_XZXLD = LDZC_ROOT + "/xzxld/index.shtml"


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ========== PERSONS DATA ==========
# The 'key' field is used for internal cross-referencing; 'name' is the display name.

persons_raw = [
    # === Core Leaders: 县委书记 & 县长 ===
    {"key": "wang_fei", "name": "王飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年6月", "birthplace": "",
     "education": "硕士研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共万荣县委员会",
     "source": URL_XWLD},
    {"key": "yi_tianliang", "name": "仪天亮", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年3月", "birthplace": "",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、县长", "current_org": "万荣县人民政府",
     "source": URL_XWLD},
    # === 县委常委 ===
    {"key": "fu_xiaoxia", "name": "付晓霞", "gender": "女", "ethnicity": "汉族",
     "birth": "1981年12月", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、万荣中学党总支书记", "current_org": "中共万荣县委员会",
     "source": URL_XWLD},
    {"key": "hu_guogang", "name": "胡国刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年12月", "birthplace": "",
     "education": "中央党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县纪委书记、县监委主任", "current_org": "中共万荣县纪律检查委员会",
     "source": URL_XWLD},
    {"key": "zhan_peng", "name": "詹鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年8月", "birthplace": "",
     "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政法委书记", "current_org": "中共万荣县委政法委员会",
     "source": URL_XWLD},
    {"key": "wang_dengfeng", "name": "王登峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1970年4月", "birthplace": "",
     "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部长", "current_org": "中共万荣县委组织部",
     "source": URL_XWLD},
    {"key": "wang_xiaolong", "name": "王肖龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年6月", "birthplace": "",
     "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长", "current_org": "万荣县人民政府",
     "source": URL_XWLD},
    {"key": "feng_qingzhong", "name": "冯清中", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年9月", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部长", "current_org": "中共万荣县委宣传部",
     "source": URL_XWLD},
    {"key": "xue_gangshan", "name": "薛钢善", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年5月", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长", "current_org": "万荣县人民政府",
     "source": URL_XWLD},
    {"key": "shao_shuizhong", "name": "邵水忠", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年8月", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、人武部部长", "current_org": "万荣县人民武装部",
     "source": URL_XWLD},
    {"key": "zhang_ruixuan", "name": "张瑞轩", "gender": "男", "ethnicity": "汉族",
     "birth": "1981年10月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、统战部长、县政协党组副书记", "current_org": "中共万荣县委统战部",
     "source": URL_XWLD},
    # === 县政府领导 (非县委常委) ===
    {"key": "shi_zhiguo", "name": "史志国", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年11月", "birthplace": "",
     "education": "中央党校大学",
     "party_join": "无党派", "work_start": "",
     "current_post": "副县长", "current_org": "万荣县人民政府",
     "source": URL_XZFLD},
    {"key": "adilijiang", "name": "阿地利江·阿不都外力", "gender": "男", "ethnicity": "维吾尔族",
     "birth": "1988年5月", "birthplace": "",
     "education": "新疆生产建设兵团委员会党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "万荣县人民政府",
     "source": URL_XZFLD},
    {"key": "huang_liuqing", "name": "黄柳青", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年3月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长、县公安局局长", "current_org": "万荣县公安局",
     "source": URL_XZFLD},
    {"key": "dong_xiaofeng", "name": "董肖峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年9月", "birthplace": "",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "万荣县人民政府",
     "source": URL_XZFLD},
    {"key": "feng_xiaofang", "name": "冯晓芳", "gender": "女", "ethnicity": "汉族",
     "birth": "1985年9月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "万荣县人民政府",
     "source": URL_XZFLD},
    # === 县人大领导 ===
    {"key": "wei_yanmei", "name": "尉艳梅", "gender": "女", "ethnicity": "汉族",
     "birth": "1971年12月", "birthplace": "",
     "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会党组书记", "current_org": "万荣县人民代表大会常务委员会",
     "source": URL_XRDLD},
    {"key": "zhang_xiaobing", "name": "张小兵", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年8月", "birthplace": "",
     "education": "大学",
     "party_join": "无党派", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "万荣县人民代表大会常务委员会",
     "source": URL_XRDLD},
    {"key": "yan_zhihong", "name": "闫志宏", "gender": "男", "ethnicity": "汉族",
     "birth": "1968年10月", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会党组成员、副主任", "current_org": "万荣县人民代表大会常务委员会",
     "source": URL_XRDLD},
    {"key": "wu_yongkai", "name": "吴永凯", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年8月", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会党组成员", "current_org": "万荣县人民代表大会常务委员会",
     "source": URL_XRDLD},
    {"key": "sun_hongwei", "name": "孙红伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年3月", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会党组成员、副主任", "current_org": "万荣县人民代表大会常务委员会",
     "source": URL_XRDLD},
    {"key": "yao_dongjie", "name": "姚东杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1968年8月", "birthplace": "",
     "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会党组成员", "current_org": "万荣县人民代表大会常务委员会",
     "source": URL_XRDLD},
    {"key": "li_zhongze", "name": "李忠泽", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年1月", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会党组成员", "current_org": "万荣县人民代表大会常务委员会",
     "source": URL_XRDLD},
    # === 县政协领导 ===
    {"key": "xu_xiaokai", "name": "徐晓凯", "gender": "男", "ethnicity": "汉族",
     "birth": "1971年5月", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协党组书记", "current_org": "中国人民政治协商会议万荣县委员会",
     "source": URL_XZXLD},
    {"key": "pan_xinhui", "name": "潘新会", "gender": "女", "ethnicity": "汉族",
     "birth": "1969年4月", "birthplace": "",
     "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协党组成员、副主席", "current_org": "中国人民政治协商会议万荣县委员会",
     "source": URL_XZXLD},
    {"key": "hu_shenying", "name": "胡慎英", "gender": "男", "ethnicity": "汉族",
     "birth": "1971年5月", "birthplace": "",
     "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协党组成员、副主席", "current_org": "中国人民政治协商会议万荣县委员会",
     "source": URL_XZXLD},
    {"key": "zhang_jinhui", "name": "张锦辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1969年6月", "birthplace": "",
     "education": "中央党校大学",
     "party_join": "无党派", "work_start": "",
     "current_post": "县政协副主席", "current_org": "中国人民政治协商会议万荣县委员会",
     "source": URL_XZXLD},
    {"key": "xie_hongyou", "name": "谢宏猷", "gender": "男", "ethnicity": "汉族",
     "birth": "1967年3月", "birthplace": "",
     "education": "大专",
     "party_join": "无党派", "work_start": "",
     "current_post": "县政协副主席", "current_org": "中国人民政治协商会议万荣县委员会",
     "source": URL_XZXLD},
    {"key": "yang_xiaokai", "name": "杨晓凯", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年8月", "birthplace": "",
     "education": "大学本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协秘书长、机关党组书记", "current_org": "中国人民政治协商会议万荣县委员会",
     "source": URL_XZXLD},
]

# Assign DB IDs
key_to_db_id = {}
for i, p in enumerate(persons_raw, 1):
    key_to_db_id[p["key"]] = i

persons = []
for i, p in enumerate(persons_raw, 1):
    persons.append({
        "id": i,
        "name": p["name"],
        "gender": p["gender"],
        "ethnicity": p["ethnicity"],
        "birth": p["birth"],
        "birthplace": p.get("birthplace", ""),
        "education": p["education"],
        "party_join": p["party_join"],
        "work_start": p.get("work_start", ""),
        "current_post": p["current_post"],
        "current_org": p["current_org"],
        "source": p["source"],
    })

organizations = [
    {"id": 1, "name": "中共万荣县委员会", "type": "party", "level": "county", "location": "万荣县"},
    {"id": 2, "name": "万荣县人民政府", "type": "government", "level": "county", "location": "万荣县"},
    {"id": 3, "name": "中共万荣县纪律检查委员会", "type": "discipline", "level": "county", "location": "万荣县"},
    {"id": 4, "name": "中共万荣县委政法委员会", "type": "party_dept", "level": "county", "location": "万荣县"},
    {"id": 5, "name": "中共万荣县委组织部", "type": "party_dept", "level": "county", "location": "万荣县"},
    {"id": 6, "name": "中共万荣县委宣传部", "type": "party_dept", "level": "county", "location": "万荣县"},
    {"id": 7, "name": "中共万荣县委统战部", "type": "party_dept", "level": "county", "location": "万荣县"},
    {"id": 8, "name": "万荣县人民武装部", "type": "government", "level": "county", "location": "万荣县"},
    {"id": 9, "name": "万荣县公安局", "type": "government", "level": "county", "location": "万荣县"},
    {"id": 10, "name": "万荣县人民代表大会常务委员会", "type": "congress", "level": "county", "location": "万荣县"},
    {"id": 11, "name": "中国人民政治协商会议万荣县委员会", "type": "cppcc", "level": "county", "location": "万荣县"},
    {"id": 12, "name": "万荣中学", "type": "education", "level": "county", "location": "万荣县"},
]

# key -> org_id
key_org = {
    "wang_fei": 1, "yi_tianliang": 2, "fu_xiaoxia": 1, "hu_guogang": 3,
    "zhan_peng": 4, "wang_dengfeng": 5, "wang_xiaolong": 2, "feng_qingzhong": 6,
    "xue_gangshan": 2, "shao_shuizhong": 8, "zhang_ruixuan": 7,
    "shi_zhiguo": 2, "adilijiang": 2, "huang_liuqing": 9,
    "dong_xiaofeng": 2, "feng_xiaofang": 2,
    "wei_yanmei": 10, "zhang_xiaobing": 10, "yan_zhihong": 10,
    "wu_yongkai": 10, "sun_hongwei": 10, "yao_dongjie": 10, "li_zhongze": 10,
    "xu_xiaokai": 11, "pan_xinhui": 11, "hu_shenying": 11,
    "zhang_jinhui": 11, "xie_hongyou": 11, "yang_xiaokai": 11,
}

positions = [
    # 县委
    {"key": "wang_fei", "org_id": 1, "title": "县委书记", "start": "", "end": "至今", "rank": "正处级"},
    {"key": "yi_tianliang", "org_id": 2, "title": "县委副书记、县长", "start": "", "end": "至今", "rank": "正处级"},
    {"key": "fu_xiaoxia", "org_id": 1, "title": "县委副书记", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "hu_guogang", "org_id": 3, "title": "县委常委、县纪委书记、县监委主任", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "zhan_peng", "org_id": 4, "title": "县委常委、政法委书记", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "wang_dengfeng", "org_id": 5, "title": "县委常委、组织部长", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "wang_xiaolong", "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "feng_qingzhong", "org_id": 6, "title": "县委常委、宣传部长", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "xue_gangshan", "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "shao_shuizhong", "org_id": 8, "title": "县委常委、人武部部长", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "zhang_ruixuan", "org_id": 7, "title": "县委常委、统战部长", "start": "", "end": "至今", "rank": "副处级"},
    # 县政府
    {"key": "shi_zhiguo", "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "adilijiang", "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "huang_liuqing", "org_id": 9, "title": "副县长、县公安局局长", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "dong_xiaofeng", "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "feng_xiaofang", "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级"},
    # 人大
    {"key": "wei_yanmei", "org_id": 10, "title": "县人大常委会党组书记", "start": "", "end": "至今", "rank": "正处级"},
    {"key": "zhang_xiaobing", "org_id": 10, "title": "县人大常委会副主任", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "yan_zhihong", "org_id": 10, "title": "县人大常委会副主任", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "wu_yongkai", "org_id": 10, "title": "县人大常委会党组成员", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "sun_hongwei", "org_id": 10, "title": "县人大常委会副主任", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "yao_dongjie", "org_id": 10, "title": "县人大常委会党组成员", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "li_zhongze", "org_id": 10, "title": "县人大常委会党组成员", "start": "", "end": "至今", "rank": "副处级"},
    # 政协
    {"key": "xu_xiaokai", "org_id": 11, "title": "县政协党组书记", "start": "", "end": "至今", "rank": "正处级"},
    {"key": "pan_xinhui", "org_id": 11, "title": "县政协副主席", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "hu_shenying", "org_id": 11, "title": "县政协副主席", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "zhang_jinhui", "org_id": 11, "title": "县政协副主席", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "xie_hongyou", "org_id": 11, "title": "县政协副主席", "start": "", "end": "至今", "rank": "副处级"},
    {"key": "yang_xiaokai", "org_id": 11, "title": "县政协秘书长", "start": "", "end": "至今", "rank": "正科级"},
    # Dual roles
    {"key": "fu_xiaoxia", "org_id": 12, "title": "万荣中学党总支书记", "start": "", "end": "至今", "rank": ""},
    {"key": "zhang_ruixuan", "org_id": 11, "title": "县政协党组副书记", "start": "", "end": "至今", "rank": "副处级"},
]

relationships = [
    ("wang_fei", "yi_tianliang", "共事", "县委书记—县长搭档", "万荣县常委会", "2024至今"),
    ("wang_fei", "fu_xiaoxia", "共事", "县委书记—副书记", "万荣县常委会", ""),
    ("wang_fei", "hu_guogang", "共事", "县委书记—纪委书记", "万荣县常委会", ""),
    ("wang_fei", "zhan_peng", "共事", "县委书记—政法委书记", "万荣县常委会", ""),
    ("wang_fei", "wang_dengfeng", "共事", "县委书记—组织部长", "万荣县常委会", ""),
    ("wang_fei", "feng_qingzhong", "共事", "县委书记—宣传部长", "万荣县常委会", ""),
    ("wang_fei", "shao_shuizhong", "共事", "县委书记—人武部长", "万荣县常委会", ""),
    ("wang_fei", "zhang_ruixuan", "共事", "县委书记—统战部长", "万荣县常委会", ""),
    ("yi_tianliang", "xue_gangshan", "共事", "县长—常务副县长", "万荣县政府党组", ""),
    ("yi_tianliang", "wang_xiaolong", "共事", "县长—副县长", "万荣县人民政府", ""),
    ("yi_tianliang", "shi_zhiguo", "共事", "县长—副县长", "万荣县人民政府", ""),
    ("yi_tianliang", "dong_xiaofeng", "共事", "县长—副县长", "万荣县人民政府", ""),
    ("yi_tianliang", "feng_xiaofang", "共事", "县长—副县长", "万荣县人民政府", ""),
    ("wang_fei", "wei_yanmei", "共事", "县委书记—人大党组书记", "万荣县四套班子", ""),
    ("yi_tianliang", "wei_yanmei", "共事", "县长—人大党组书记", "万荣县四套班子", ""),
    ("wei_yanmei", "xu_xiaokai", "共事", "人大党组书记—政协党组书记", "万荣县四套班子", ""),
    ("wang_fei", "xu_xiaokai", "共事", "县委书记—政协党组书记", "万荣县四套班子", ""),
    ("yi_tianliang", "adilijiang", "共事", "县长—副县长", "万荣县人民政府", ""),
    ("xue_gangshan", "wang_xiaolong", "共事", "副县长（同事）", "万荣县人民政府", ""),
]

# ========== BUILD DATABASE ==========
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")

conn.execute("DROP TABLE IF EXISTS relationships")
conn.execute("DROP TABLE IF EXISTS positions")
conn.execute("DROP TABLE IF EXISTS organizations")
conn.execute("DROP TABLE IF EXISTS persons")

conn.execute("""
CREATE TABLE persons (
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
)
""")
conn.execute("""
CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT DEFAULT '',
    level TEXT DEFAULT '',
    parent TEXT DEFAULT '',
    location TEXT DEFAULT ''
)
""")
conn.execute("""
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT DEFAULT '',
    start_date TEXT DEFAULT '',
    end_date TEXT DEFAULT '',
    rank TEXT DEFAULT '',
    note TEXT DEFAULT '',
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
)
""")
conn.execute("""
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT DEFAULT '',
    context TEXT DEFAULT '',
    overlap_org TEXT DEFAULT '',
    overlap_period TEXT DEFAULT '',
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
)
""")

for p in persons:
    conn.execute(
        "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"], p["current_post"],
         p["current_org"], p["source"])
    )

for o in organizations:
    conn.execute(
        "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
        (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o["location"])
    )

for pos in positions:
    conn.execute(
        "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank) VALUES (?,?,?,?,?,?)",
        (key_to_db_id[pos["key"]], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"])
    )

for ra in relationships:
    conn.execute(
        "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
        (key_to_db_id[ra[0]], key_to_db_id[ra[1]], ra[2], ra[3], ra[4], ra[5])
    )

conn.commit()
conn.close()

print(f"[DB] Written to: {DB_PATH}")
print(f"     {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

# ========== BUILD GEXF ==========
lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>万荣县领导班子关系图</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="role" title="role" type="string"/>')
lines.append('    </attributes>')
# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="relation_type" title="relation_type" type="string"/>')
lines.append('      <attribute id="context" title="context" type="string"/>')
lines.append('      <attribute id="overlap_org" title="overlap_org" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    post = p["current_post"] or ""
    if "县委书记" in post and "副书记" not in post:
        color, sz = "255,50,50", "20.0"
    elif "县长" in post:
        color, sz = "50,100,255", "20.0"
    elif "纪委书记" in post:
        color, sz = "255,165,0", "12.0"
    elif "副书记" in post:
        color, sz = "50,100,255", "15.0"
    elif "人大" in post:
        color, sz = "200,255,255", "12.0"
    elif "政协" in post:
        color, sz = "255,240,200", "12.0"
    else:
        color, sz = "100,100,100", "12.0"
    cr, cg, cb = color.split(",")
    lines.append(f'      <node id="{esc(p["name"])}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{esc(post)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Org nodes
org_colors = {
    "party": "255,200,200", "government": "200,200,255", "discipline": "255,200,200",
    "party_dept": "255,200,200", "congress": "200,255,255", "cppcc": "255,240,200",
    "education": "200,255,200",
}
for o in organizations:
    oc = org_colors.get(o["type"], "200,200,200")
    cr, cg, cb = oc.split(",")
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    name = persons[key_to_db_id[pos["key"]] - 1]["name"]
    lines.append(f'      <edge id="e{eid}" source="{name}" target="o{pos["org_id"]}" label="worked_at" type="directed">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="relation_type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for ra in relationships:
    eid += 1
    name_a = persons[key_to_db_id[ra[0]] - 1]["name"]
    name_b = persons[key_to_db_id[ra[1]] - 1]["name"]
    lines.append(f'      <edge id="e{eid}" source="{name_a}" target="{name_b}" label="{ra[2]}" type="undirected">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="relation_type" value="{ra[2]}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(ra[3])}"/>')
    lines.append(f'          <attvalue for="overlap_org" value="{esc(ra[4])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"[GEXF] Written to: {GEXF_PATH}")
print("[Done] build_万荣县_data.py completed.")