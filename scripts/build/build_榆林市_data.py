#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 榆林市 (Yulin City, Shaanxi) leadership network."""

import sqlite3
import os
import sys

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "榆林市"
DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── A. City-level leadership ──
    # 市委
    {"id": 1, "name": "张胜利", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-12", "birthplace": "", "education": "研究生",
     "party_join": "", "work_start": "",
     "current_post": "榆林市委书记", "current_org": "中共榆林市委",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/sw/sj/zsl/"},
    {"id": 2, "name": "马月逢", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-05", "birthplace": "", "education": "大学",
     "party_join": "", "work_start": "",
     "current_post": "榆林市委副书记、市长", "current_org": "榆林市人民政府",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/sw/fsj/myf/"},
    {"id": 3, "name": "牛钧", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-08", "birthplace": "", "education": "大学",
     "party_join": "", "work_start": "",
     "current_post": "榆林市委常委、纪委书记、监委主任", "current_org": "中共榆林市纪委",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/sw/cw/nj/"},
    {"id": 4, "name": "贺湘如", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "研究生",
     "party_join": "", "work_start": "",
     "current_post": "榆林市委常委、副市长", "current_org": "榆林市人民政府",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/sw/cw/hxr/"},
    {"id": 5, "name": "谢杉", "gender": "女", "ethnicity": "汉族",
     "birth": "1981-06", "birthplace": "", "education": "研究生",
     "party_join": "", "work_start": "",
     "current_post": "榆林市委常委、组织部部长", "current_org": "中共榆林市委组织部",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/sw/cw/xs/"},
    {"id": 6, "name": "黄继", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-11", "birthplace": "", "education": "研究生",
     "party_join": "", "work_start": "",
     "current_post": "榆林市委常委、军分区大校司令员", "current_org": "榆林军分区",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/sw/cw/hj/"},
    {"id": 7, "name": "徐刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-06", "birthplace": "", "education": "大学",
     "party_join": "", "work_start": "",
     "current_post": "榆林市委常委、宣传部部长", "current_org": "中共榆林市委宣传部",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/sw/cw/xg1/"},
    {"id": 8, "name": "杨德邦", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-11", "birthplace": "", "education": "大学",
     "party_join": "", "work_start": "",
     "current_post": "榆林市委常委、副市长", "current_org": "榆林市人民政府",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/sw/cw/ydb/"},
    {"id": 9, "name": "陈治忠", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-12", "birthplace": "", "education": "研究生",
     "party_join": "", "work_start": "",
     "current_post": "榆林市委秘书长", "current_org": "中共榆林市委办公室",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/sw/msz/czz/"},
    # 市政府 (非市委常委的副市长)
    {"id": 10, "name": "雷纯", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市副市长", "current_org": "榆林市人民政府",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szf/fsz/lc/"},
    {"id": 11, "name": "张保航", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市副市长", "current_org": "榆林市人民政府",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szf/fsz/zbh/"},
    {"id": 12, "name": "沈效功", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市副市长", "current_org": "榆林市人民政府",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szf/fsz/sxf/"},
    {"id": 13, "name": "姬跃飞", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市副市长", "current_org": "榆林市人民政府",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szf/fsz/jyf/"},
    {"id": 14, "name": "田小宁", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市副市长", "current_org": "榆林市人民政府",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szf/fsz/txn/"},
    {"id": 15, "name": "吕瑞卿", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市政府秘书长", "current_org": "榆林市人民政府办公室",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szf/msz/lrq/"},
    # 市人大常委会
    {"id": 16, "name": "王国忠", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市人大常委会主任", "current_org": "榆林市人大常委会",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/srdcwh/zr/wgz/"},
    {"id": 17, "name": "高明伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市人大常委会副主任", "current_org": "榆林市人大常委会",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/srdcwh/fzr/gmw/"},
    {"id": 18, "name": "常少海", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市人大常委会副主任", "current_org": "榆林市人大常委会",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/srdcwh/fzr/csh/"},
    {"id": 19, "name": "冯光宏", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市人大常委会副主任", "current_org": "榆林市人大常委会",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/srdcwh/fzr/fgh/"},
    {"id": 20, "name": "贺耀东", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市人大常委会副主任", "current_org": "榆林市人大常委会",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/srdcwh/fzr/hyd/"},
    {"id": 21, "name": "米劲", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市人大常委会副主任", "current_org": "榆林市人大常委会",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/srdcwh/fzr/mj/"},
    {"id": 22, "name": "封杰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市人大常委会副主任", "current_org": "榆林市人大常委会",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/srdcwh/fzr/fj/"},
    {"id": 23, "name": "杨文慧", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市人大常委会副主任", "current_org": "榆林市人大常委会",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/srdcwh/fzr/ywh/"},
    {"id": 24, "name": "杨啸中", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市人大常委会秘书长", "current_org": "榆林市人大常委会",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/srdcwh/msz/yxz/"},
    # 市政协
    {"id": 25, "name": "王华胜", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市政协党组书记、主席", "current_org": "榆林市政协",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szx/zr/whs/"},
    {"id": 26, "name": "高怀和", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市政协副主席", "current_org": "榆林市政协",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szx/fzr/ghh/"},
    {"id": 27, "name": "任静波", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市政协副主席", "current_org": "榆林市政协",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szx/fzr/rjb/"},
    {"id": 28, "name": "王志强", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市政协副主席", "current_org": "榆林市政协",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szx/fzr/wzq/"},
    {"id": 29, "name": "拓耀飞", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市政协副主席", "current_org": "榆林市政协",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szx/fzr/tyf/"},
    {"id": 30, "name": "姬世平", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市政协副主席", "current_org": "榆林市政协",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szx/fzr/jsp/"},
    {"id": 31, "name": "许君", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市政协副主席", "current_org": "榆林市政协",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szx/fzr/xj/"},
    {"id": 32, "name": "谢宏", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "榆林市政协秘书长", "current_org": "榆林市政协",
     "source": "https://www.yl.gov.cn/zwgk/fdzdgknr/ldzc/szx/msz/xh/"},
]

organizations = [
    {"id": 1, "name": "中共榆林市委", "type": "党委", "level": "地级市", "parent": "中共陕西省委", "location": "陕西省榆林市"},
    {"id": 2, "name": "榆林市人民政府", "type": "政府", "level": "地级市", "parent": "陕西省人民政府", "location": "陕西省榆林市"},
    {"id": 3, "name": "中共榆林市纪委", "type": "纪委", "level": "地级市", "parent": "中共榆林市委", "location": "陕西省榆林市"},
    {"id": 4, "name": "榆林市监察委员会", "type": "政府", "level": "地级市", "parent": "榆林市人民政府", "location": "陕西省榆林市"},
    {"id": 5, "name": "中共榆林市委组织部", "type": "党委", "level": "地级市", "parent": "中共榆林市委", "location": "陕西省榆林市"},
    {"id": 6, "name": "榆林军分区", "type": "军队", "level": "地级市", "parent": "陕西省军区", "location": "陕西省榆林市"},
    {"id": 7, "name": "中共榆林市委宣传部", "type": "党委", "level": "地级市", "parent": "中共榆林市委", "location": "陕西省榆林市"},
    {"id": 8, "name": "中共榆林市委办公室", "type": "党委", "level": "地级市", "parent": "中共榆林市委", "location": "陕西省榆林市"},
    {"id": 9, "name": "榆林市人民政府办公室", "type": "政府", "level": "地级市", "parent": "榆林市人民政府", "location": "陕西省榆林市"},
    {"id": 10, "name": "榆林市人大常委会", "type": "人大", "level": "地级市", "parent": "", "location": "陕西省榆林市"},
    {"id": 11, "name": "榆林市政协", "type": "政协", "level": "地级市", "parent": "", "location": "陕西省榆林市"},
]

positions = [
    # 张胜利
    {"person_id": 1, "org_id": 1, "title": "榆林市委书记", "start_date": "", "end_date": "present", "rank": "正厅级"},
    # 马月逢
    {"person_id": 2, "org_id": 1, "title": "榆林市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级"},
    {"person_id": 2, "org_id": 2, "title": "榆林市市长", "start_date": "", "end_date": "present", "rank": "正厅级"},
    # 牛钧
    {"person_id": 3, "org_id": 1, "title": "榆林市委常委", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 3, "org_id": 3, "title": "榆林市纪委书记", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 3, "org_id": 4, "title": "榆林市监委主任", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 贺湘如
    {"person_id": 4, "org_id": 1, "title": "榆林市委常委", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 4, "org_id": 2, "title": "榆林市副市长", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 谢杉
    {"person_id": 5, "org_id": 1, "title": "榆林市委常委", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 5, "org_id": 5, "title": "榆林市委组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 黄继
    {"person_id": 6, "org_id": 1, "title": "榆林市委常委", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 6, "org_id": 6, "title": "榆林军分区大校司令员", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 徐刚
    {"person_id": 7, "org_id": 1, "title": "榆林市委常委", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 7, "org_id": 7, "title": "榆林市委宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 杨德邦
    {"person_id": 8, "org_id": 1, "title": "榆林市委常委", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 8, "org_id": 2, "title": "榆林市副市长", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 陈治忠
    {"person_id": 9, "org_id": 8, "title": "榆林市委秘书长", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 雷纯
    {"person_id": 10, "org_id": 2, "title": "榆林市副市长", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 张保航
    {"person_id": 11, "org_id": 2, "title": "榆林市副市长", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 沈效功
    {"person_id": 12, "org_id": 2, "title": "榆林市副市长", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 姬跃飞
    {"person_id": 13, "org_id": 2, "title": "榆林市副市长", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 田小宁
    {"person_id": 14, "org_id": 2, "title": "榆林市副市长", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 吕瑞卿
    {"person_id": 15, "org_id": 9, "title": "榆林市政府秘书长", "start_date": "", "end_date": "present", "rank": "正处级"},
    # 市人大常委会
    {"person_id": 16, "org_id": 10, "title": "榆林市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级"},
    {"person_id": 17, "org_id": 10, "title": "榆林市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 18, "org_id": 10, "title": "榆林市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 19, "org_id": 10, "title": "榆林市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 20, "org_id": 10, "title": "榆林市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 21, "org_id": 10, "title": "榆林市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 22, "org_id": 10, "title": "榆林市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 23, "org_id": 10, "title": "榆林市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 24, "org_id": 10, "title": "榆林市人大常委会秘书长", "start_date": "", "end_date": "present", "rank": "正处级"},
    # 市政协
    {"person_id": 25, "org_id": 11, "title": "榆林市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级"},
    {"person_id": 26, "org_id": 11, "title": "榆林市政协副主席", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 27, "org_id": 11, "title": "榆林市政协副主席", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 28, "org_id": 11, "title": "榆林市政协副主席", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 29, "org_id": 11, "title": "榆林市政协副主席", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 30, "org_id": 11, "title": "榆林市政协副主席", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 31, "org_id": 11, "title": "榆林市政协副主席", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 32, "org_id": 11, "title": "榆林市政协秘书长", "start_date": "", "end_date": "present", "rank": "正处级"},
]

relationships = [
    # 张胜利 → 马月逢：党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "党政一把手搭档（书记—市长）", "overlap_org": "中共榆林市委", "overlap_period": "present"},
    # 张胜利 → 牛钧：党委—纪委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "纪委书记对市委书记负责", "overlap_org": "中共榆林市委", "overlap_period": "present"},
    # 张胜利 → 谢杉：党委—组织部
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "组织部长受市委书记领导", "overlap_org": "中共榆林市委", "overlap_period": "present"},
    # 张胜利 → 贺湘如：党委—政府交叉任职
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委常委、副市长受书记领导", "overlap_org": "中共榆林市委", "overlap_period": "present"},
    # 张胜利 → 徐刚：党委—宣传部
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "宣传部长受市委书记领导", "overlap_org": "中共榆林市委", "overlap_period": "present"},
    # 张胜利 → 杨德邦
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "市委常委、副市长受书记领导", "overlap_org": "中共榆林市委", "overlap_period": "present"},
    # 马月逢 → 贺湘如：市长—副市长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "市长—副市长（市政府领导班子）", "overlap_org": "榆林市人民政府", "overlap_period": "present"},
    # 马月逢 → 杨德邦
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "市长—副市长（市政府领导班子）", "overlap_org": "榆林市人民政府", "overlap_period": "present"},
    # 马月逢 → 其他副市长
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "榆林市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "榆林市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "榆林市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "榆林市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "榆林市人民政府", "overlap_period": "present"},
    # 贺湘如 — 杨德邦：同为市委常委、副市长
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "同为市委常委、副市长", "overlap_org": "中共榆林市委", "overlap_period": "present"},
    # 牛钧 — 谢杉：纪委—组织部协作
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "纪委—组织部协作（干部监督）", "overlap_org": "中共榆林市委", "overlap_period": "present"},
]

# ── BUILD ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
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
    print("✓ Build complete for 榆林市")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")
