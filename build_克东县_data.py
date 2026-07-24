#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 克东县 leadership network.

克东县隶属黑龙江省齐齐哈尔市。

Current leadership as of 2026-07 (source: www.kedong.gov.cn 领导之窗):
- 县委书记: 梁兴旺 (男, 汉族, 1974年2月, 大学)
- 县长: 许晓飞 (男, 汉族, 1979年5月, 大学)
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "克东县"
DB_PATH = DATABASE_DIR / "克东县_network.db"
GEXF_PATH = GRAPH_DIR / "克东县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共克东县委员会", "type": "党委", "level": "县处级", "parent": "中共齐齐哈尔市委", "location": "黑龙江省齐齐哈尔市克东县"},
    {"id": 2, "name": "克东县人民政府", "type": "政府", "level": "县处级", "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市克东县"},
    {"id": 3, "name": "克东县人大常委会", "type": "人大", "level": "县处级", "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市克东县"},
    {"id": 4, "name": "克东县政协", "type": "政协", "level": "县处级", "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市克东县"},
    {"id": 5, "name": "中共克东县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共齐齐哈尔市纪委", "location": "黑龙江省齐齐哈尔市克东县"},
    {"id": 6, "name": "中共克东县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共克东县委员会", "location": "黑龙江省齐齐哈尔市克东县"},
    {"id": 7, "name": "中共克东县委组织部", "type": "党委", "level": "县处级", "parent": "中共克东县委员会", "location": "黑龙江省齐齐哈尔市克东县"},
    {"id": 8, "name": "中共克东县委宣传部", "type": "党委", "level": "县处级", "parent": "中共克东县委员会", "location": "黑龙江省齐齐哈尔市克东县"},
    {"id": 9, "name": "中共克东县委统战部", "type": "党委", "level": "县处级", "parent": "中共克东县委员会", "location": "黑龙江省齐齐哈尔市克东县"},
    {"id": 10, "name": "中共克东县委办公室", "type": "党委", "level": "县处级", "parent": "中共克东县委员会", "location": "黑龙江省齐齐哈尔市克东县"},
    {"id": 11, "name": "克东县公安局", "type": "政府", "level": "县处级", "parent": "克东县人民政府", "location": "黑龙江省齐齐哈尔市克东县"},
    {"id": 12, "name": "克东县人民武装部", "type": "政府", "level": "县处级", "parent": "齐齐哈尔军分区", "location": "黑龙江省齐齐哈尔市克东县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────

persons = [
    # ── 县委领导 ──
    # 1. 梁兴旺 — 县委书记
    {"id": 1, "name": "梁兴旺", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年2月", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县委书记", "current_org": "中共克东县委员会",
     "source": "https://www.kedong.gov.cn/kedong/c103708/202009/c02_cc137f022cf748c5a00d3b38a5bd0c06.shtml"},
    # 2. 许晓飞 — 县委副书记、县长
    {"id": 2, "name": "许晓飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年5月", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县委副书记、县政府县长", "current_org": "克东县人民政府",
     "source": "https://www.kedong.gov.cn/kedong/c103713/202011/c02_481430.shtml"},
    # 3. 刘士辉 — 县委副书记、统战部部长
    {"id": 3, "name": "刘士辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1985年12月", "birthplace": "", "education": "硕士研究生学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县委副书记、统战部部长", "current_org": "中共克东县委员会",
     "source": "https://www.kedong.gov.cn/kedong/c103709/202310/c02_371163.shtml"},
    # 4. 冯立军 — 县委常委、纪委书记、监委主任
    {"id": 4, "name": "冯立军", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年5月", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县委常委、纪委书记、监委主任", "current_org": "中共克东县纪律检查委员会",
     "source": "https://www.kedong.gov.cn/kedong/c103710/202009/c02_999cdb18443f4c89b0b8b0314f19a900.shtml"},
    # 5. 梁永峰 — 县委常委、宣传部部长
    {"id": 5, "name": "梁永峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年6月", "birthplace": "", "education": "在职研究生学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县委常委、宣传部部长", "current_org": "中共克东县委宣传部",
     "source": "https://www.kedong.gov.cn/kedong/c103710/202011/c02_bd57f01722e549eaaef0b26337a23c59.shtml"},
    # 6. 刘国范 — 县委常委、常务副县长
    {"id": 6, "name": "刘国范", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年12月", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县委常委、县政府副县长（常务）", "current_org": "克东县人民政府",
     "source": "https://www.kedong.gov.cn/kedong/c103710/202111/c02_b4f0726e244147dfad1e8c9896c76a5b.shtml"},
    # 7. 孟祥媛 — 县委常委、组织部部长
    {"id": 7, "name": "孟祥媛", "gender": "女", "ethnicity": "汉族",
     "birth": "1973年12月", "birthplace": "", "education": "大专学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县委常委、组织部部长", "current_org": "中共克东县委组织部",
     "source": "https://www.kedong.gov.cn/kedong/c103710/202011/c02_6174ce1e86e74134856823dbead4b709.shtml"},
    # 8. 李耀华 — 县委常委、政法委书记
    {"id": 8, "name": "李耀华", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年11月", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县委常委、政法委书记", "current_org": "中共克东县委政法委员会",
     "source": "https://www.kedong.gov.cn/kedong/c103710/202009/c02_4e094298233149d29be7b5de26d3fd5f.shtml"},
    # 9. 李金成 — 县委常委、县委办主任
    {"id": 9, "name": "李金成", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年12月", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县委常委、县委办主任", "current_org": "中共克东县委办公室",
     "source": "https://www.kedong.gov.cn/kedong/c103710/202406/c02_475277.shtml"},
    # 10. 郑皓月 — 县委常委、副县长（挂职）
    {"id": 10, "name": "郑皓月", "gender": "女", "ethnicity": "蒙古族",
     "birth": "1990年6月", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县委常委、县政府副县长（挂职）", "current_org": "克东县人民政府",
     "source": "https://www.kedong.gov.cn/kedong/c103710/202506/c02_554799.shtml"},
    # 11. 陈文平 — 县委常委、人武部政委
    {"id": 11, "name": "陈文平", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年11月", "birthplace": "", "education": "本科",
     "party_join": "", "work_start": "",
     "current_post": "克东县委常委、人武部上校政治委员", "current_org": "克东县人民武装部",
     "source": "https://www.kedong.gov.cn/kedong/c103710/202603/c02_613932.shtml"},
    # ── 县政府副县长（非常委）──
    # 12. 王效哲 — 副县长
    {"id": 12, "name": "王效哲", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年2月", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县政府副县长", "current_org": "克东县人民政府",
     "source": "https://www.kedong.gov.cn/kedong/c103714/202310/c02_371165.shtml"},
    # 13. 刘莉霜 — 副县长
    {"id": 13, "name": "刘莉霜", "gender": "女", "ethnicity": "汉族",
     "birth": "1973年6月", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县政府副县长", "current_org": "克东县人民政府",
     "source": "https://www.kedong.gov.cn/kedong/c103714/202110/c02_0bf89b4f11e24326a91c2683db639932.shtml"},
    # 14. 宋宏大 — 副县长
    {"id": 14, "name": "宋宏大", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年6月", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县政府副县长", "current_org": "克东县人民政府",
     "source": "https://www.kedong.gov.cn/kedong/c103714/202409/c02_496194.shtml"},
    # 15. 王晓明 — 副县长、公安局局长
    {"id": 15, "name": "王晓明", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年11月", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县政府副县长、公安局局长", "current_org": "克东县人民政府",
     "source": "https://www.kedong.gov.cn/kedong/c103714/202009/c02_7270edbc2c70458ca13a6310920cadd9.shtml"},
    # 16. 刘武增 — 副县长
    {"id": 16, "name": "刘武增", "gender": "男", "ethnicity": "汉族",
     "birth": "1988年1月", "birthplace": "", "education": "研究生学历",
     "party_join": "", "work_start": "",
     "current_post": "克东县政府副县长", "current_org": "克东县人民政府",
     "source": "https://www.kedong.gov.cn/kedong/c103714/202601/c02_604128.shtml"},
    # ── 人大、政协 ──
    # 17. 张立军 — 县人大常委会主任
    {"id": 17, "name": "张立军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克东县人大常委会主任", "current_org": "克东县人大常委会",
     "source": "https://www.kedong.gov.cn/kedong/c103711/202009/c02_cc8871c6e87d4b02b3e89a7d601d75b6.shtml"},
    # 18. 刘畅 — 县政协主席
    {"id": 18, "name": "刘畅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克东县政协主席", "current_org": "克东县政协",
     "source": "https://www.kedong.gov.cn/kedong/c103715/202601/c02_599378.shtml"},
]

# ── POSITIONS ──────────────────────────────────────────────────────

positions = [
    # 梁兴旺
    {"person_id": 1, "org_id": 1, "title": "克东县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县委全面工作"},
    # 许晓飞
    {"person_id": 2, "org_id": 1, "title": "克东县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "克东县政府县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县政府全面工作"},
    # 刘士辉
    {"person_id": 3, "org_id": 1, "title": "克东县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管统战部"},
    {"person_id": 3, "org_id": 9, "title": "克东县委统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 冯立军
    {"person_id": 4, "org_id": 1, "title": "克东县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "克东县纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "主持县纪委监委全面工作"},
    # 梁永峰
    {"person_id": 5, "org_id": 1, "title": "克东县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 8, "title": "克东县委宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 刘国范
    {"person_id": 6, "org_id": 1, "title": "克东县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "克东县政府副县长（常务）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责县政府常务工作"},
    # 孟祥媛
    {"person_id": 7, "org_id": 1, "title": "克东县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "克东县委组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 李耀华
    {"person_id": 8, "org_id": 1, "title": "克东县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "克东县委政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 李金成
    {"person_id": 9, "org_id": 1, "title": "克东县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 10, "title": "克东县委办主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 郑皓月
    {"person_id": 10, "org_id": 1, "title": "克东县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "克东县政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 陈文平
    {"person_id": 11, "org_id": 1, "title": "克东县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 12, "title": "克东县人武部上校政治委员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 王效哲
    {"person_id": 12, "org_id": 2, "title": "克东县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 刘莉霜
    {"person_id": 13, "org_id": 2, "title": "克东县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 宋宏大
    {"person_id": 14, "org_id": 2, "title": "克东县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 王晓明
    {"person_id": 15, "org_id": 2, "title": "克东县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 11, "title": "克东县公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 刘武增
    {"person_id": 16, "org_id": 2, "title": "克东县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 张立军
    {"person_id": 17, "org_id": 3, "title": "克东县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 刘畅
    {"person_id": 18, "org_id": 4, "title": "克东县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────

relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委班子党政正职搭档", "overlap_org": "中共克东县委员会/克东县人民政府", "overlap_period": ""},
    # 梁兴旺 — 刘士辉（书记—副书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与专职副书记", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    # 许晓飞 — 刘士辉（县长—副书记）
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县政府县长与县委副书记同班子", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    # 许晓飞 — 刘国范（县长—常务副县长工作关系）
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与常务副县长（协助分管财政、审计）", "overlap_org": "克东县人民政府", "overlap_period": ""},
    # 许晓飞 — 刘武增（县长—副县长，协助分管经开区）
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "县长与副县长（协助分管县经开区管委会）", "overlap_org": "克东县人民政府", "overlap_period": ""},
    # 刘士辉 — 李耀华（副书记协管信访+政法委书记）
    {"person_a": 3, "person_b": 8, "type": "superior_subordinate", "context": "县委副书记（分管信访）与政法委书记（协助抓信访）", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    # 刘士辉 — 孟祥媛（副书记—组织部长）
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "县委副书记与组织部部长同班子", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    # 刘士辉 — 李金成（副书记—县委办，协助副书记抓改革、考评）
    {"person_a": 3, "person_b": 9, "type": "superior_subordinate", "context": "县委副书记与县委办主任（协助抓改革和督考）", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    # 梁兴旺 — 李金成（书记—县委办主任，协助书记抓招商）
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记与县委办主任（协助抓招商引资）", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    # 梁兴旺 — 冯立军（书记—纪委书记）
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    # 县委常委班子（全体常委同班子关系）
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 11, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 9, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 10, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 11, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 9, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 10, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 11, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 9, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 10, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 11, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 10, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 11, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 11, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共克东县委员会", "overlap_period": ""},
    # 县政府领导班子（副县长）
    {"person_a": 12, "person_b": 13, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "克东县人民政府", "overlap_period": ""},
    {"person_a": 12, "person_b": 14, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "克东县人民政府", "overlap_period": ""},
    {"person_a": 12, "person_b": 15, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "克东县人民政府", "overlap_period": ""},
    {"person_a": 12, "person_b": 16, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "克东县人民政府", "overlap_period": ""},
    {"person_a": 13, "person_b": 14, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "克东县人民政府", "overlap_period": ""},
    {"person_a": 13, "person_b": 15, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "克东县人民政府", "overlap_period": ""},
    {"person_a": 13, "person_b": 16, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "克东县人民政府", "overlap_period": ""},
    {"person_a": 14, "person_b": 15, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "克东县人民政府", "overlap_period": ""},
    {"person_a": 14, "person_b": 16, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "克东县人民政府", "overlap_period": ""},
    {"person_a": 15, "person_b": 16, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "克东县人民政府", "overlap_period": ""},
]

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
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
