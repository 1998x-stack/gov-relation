#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 讷河市 leadership network.

讷河市隶属于黑龙江省齐齐哈尔市，县级市。

Current leadership as of 2026-07 (source: www.nehe.gov.cn):
- 市委书记: 王永平 (born 1970.8)
- 市长: 栾云巍 (born 1979.12)
"""

import sqlite3
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "讷河市"

# Write to staging directory
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "讷河市_network.db"
GEXF_PATH = STAGING_DIR / "讷河市_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────

organizations = [
    # 党委
    {"id": 1, "name": "中共讷河市委员会", "type": "党委", "level": "县处级", "parent": "中共齐齐哈尔市委", "location": "黑龙江省齐齐哈尔市讷河市"},
    # 纪委
    {"id": 2, "name": "中共讷河市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共齐齐哈尔市纪委", "location": "黑龙江省齐齐哈尔市讷河市"},
    # 政府
    {"id": 3, "name": "讷河市人民政府", "type": "政府", "level": "县处级", "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市讷河市"},
    # 人大
    {"id": 4, "name": "讷河市人大常委会", "type": "人大", "level": "县处级", "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市讷河市"},
    # 政协
    {"id": 5, "name": "讷河市政协", "type": "政协", "level": "县处级", "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市讷河市"},
    # 党委部门
    {"id": 6, "name": "中共讷河市委政法委员会", "type": "党委", "level": "县处级", "parent": "中共讷河市委员会", "location": "黑龙江省齐齐哈尔市讷河市"},
    {"id": 7, "name": "中共讷河市委组织部", "type": "党委", "level": "县处级", "parent": "中共讷河市委员会", "location": "黑龙江省齐齐哈尔市讷河市"},
    {"id": 8, "name": "中共讷河市委宣传部", "type": "党委", "level": "县处级", "parent": "中共讷河市委员会", "location": "黑龙江省齐齐哈尔市讷河市"},
    {"id": 9, "name": "中共讷河市委统战部", "type": "党委", "level": "县处级", "parent": "中共讷河市委员会", "location": "黑龙江省齐齐哈尔市讷河市"},
    {"id": 10, "name": "讷河市人民武装部", "type": "党委", "level": "县处级", "parent": "齐齐哈尔军分区", "location": "黑龙江省齐齐哈尔市讷河市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────

persons = [
    # ── 市委领导 ──
    {"id": 1, "name": "王永平", "gender": "男", "ethnicity": "汉族",
     "birth": "1970年8月", "birthplace": "", "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共讷河市委书记、党校校长", "current_org": "中共讷河市委员会",
     "source": "https://www.nehe.gov.cn/nehe/c100476/202307/c02_c9fce03da2264daf99f8119cfd052096.shtml"},
    {"id": 2, "name": "栾云巍", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年12月", "birthplace": "", "education": "在职大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共讷河市委副书记、市政府党组书记、市长", "current_org": "讷河市人民政府",
     "source": "https://www.nehe.gov.cn/nehe/c100476/202307/c02_b3f4cb2164ec44f487e2a459d41597bb.shtml"},
    {"id": 3, "name": "李青春", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年8月", "birthplace": "", "education": "大学学历，学士学位",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共讷河市委副书记、统战部部长、政协党组副书记", "current_org": "中共讷河市委员会",
     "source": "https://www.nehe.gov.cn/nehe/c100476/202307/c02_9a503f6a96414148be02dd0862416d2f.shtml"},
    {"id": 4, "name": "唐守志", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年2月", "birthplace": "", "education": "在职大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共讷河市委常委、市政府党组成员、副市长", "current_org": "中共讷河市委员会",
     "source": "https://www.nehe.gov.cn/nehe/c100476/202401/c02_440273.shtml"},
    {"id": 5, "name": "战伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1970年7月", "birthplace": "", "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共讷河市委常委、政法委书记", "current_org": "中共讷河市委员会",
     "source": "https://www.nehe.gov.cn/nehe/c100476/202307/c02_21ab71440ef7492eb1748240fe1023e0.shtml"},
    {"id": 6, "name": "刘宽", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年2月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共讷河市委常委、纪委书记、监委主任", "current_org": "中共讷河市纪律检查委员会",
     "source": "https://www.nehe.gov.cn/nehe/c100476/202601/c02_600090.shtml"},
    {"id": 7, "name": "王磊", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年5月", "birthplace": "", "education": "在职大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共讷河市委常委、组织部部长", "current_org": "中共讷河市委员会",
     "source": "https://www.nehe.gov.cn/nehe/c100476/202510/c02_581410.shtml"},
    {"id": 8, "name": "宋金英", "gender": "女", "ethnicity": "汉族",
     "birth": "1976年1月", "birthplace": "", "education": "在职大专学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共讷河市委常委、宣传部部长", "current_org": "中共讷河市委员会",
     "source": "https://www.nehe.gov.cn/nehe/c100476/202307/c02_314238c3e340484faab7552cdbbca195.shtml"},
    {"id": 9, "name": "徐渤程", "gender": "男", "ethnicity": "汉族",
     "birth": "1985年9月", "birthplace": "", "education": "在职研究生学历，硕士学位",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共讷河市委常委、市政府党组副书记、副市长", "current_org": "中共讷河市委员会",
     "source": "https://www.nehe.gov.cn/nehe/c100476/202309/c02_311054.shtml"},
    {"id": 10, "name": "董亮", "gender": "男", "ethnicity": "汉族",
     "birth": "1981年2月", "birthplace": "", "education": "大学学历，学士学位",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共讷河市委常委、人民武装部上校政治委员", "current_org": "讷河市人民武装部",
     "source": "https://www.nehe.gov.cn/nehe/c100476/202501/c02_519879.shtml"},
    # ── 市政府其他领导 ──
    {"id": 11, "name": "刘广伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年9月", "birthplace": "", "education": "在职大专学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "讷河市政府党组成员、副市长", "current_org": "讷河市人民政府",
     "source": "https://www.nehe.gov.cn/nehe/c100478/202307/c02_0db0cac3117849b48e4ed0f2b1d9eda3.shtml"},
    {"id": 12, "name": "冯雪光", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年10月", "birthplace": "", "education": "大学学历，学士学位",
     "party_join": "中共党员", "work_start": "",
     "current_post": "讷河市政府党组成员、副市长", "current_org": "讷河市人民政府",
     "source": "https://www.nehe.gov.cn/nehe/c100478/202309/c02_311055.shtml"},
    {"id": 13, "name": "马玉洁", "gender": "女", "ethnicity": "汉族",
     "birth": "1983年3月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "讷河市政府党组成员、副市长", "current_org": "讷河市人民政府",
     "source": "https://www.nehe.gov.cn/nehe/c100478/202309/c02_311056.shtml"},
    {"id": 14, "name": "李长宝", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年4月", "birthplace": "", "education": "在职大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "讷河市政府副市长", "current_org": "讷河市人民政府",
     "source": "https://www.nehe.gov.cn/nehe/c100478/202507/c02_565812.shtml"},
    # ── 市人大 ──
    {"id": 15, "name": "东宇辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1967年1月", "birthplace": "", "education": "在职大学学历，硕士学位",
     "party_join": "中共党员", "work_start": "",
     "current_post": "讷河市人大常委会主任、党组书记", "current_org": "讷河市人大常委会",
     "source": "https://www.nehe.gov.cn/nehe/c100477/202307/c02_7f0a9767f3c1451d9f9245ae28668952.shtml"},
    {"id": 16, "name": "朱凤春", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "讷河市人大常委会副主任", "current_org": "讷河市人大常委会",
     "source": "https://www.nehe.gov.cn/nehe/c100477/redirect_firstArticle.shtml"},
    {"id": 17, "name": "杨振宇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "讷河市人大常委会副主任", "current_org": "讷河市人大常委会",
     "source": "https://www.nehe.gov.cn/nehe/c100477/redirect_firstArticle.shtml"},
    {"id": 18, "name": "赵福元", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "讷河市人大常委会副主任", "current_org": "讷河市人大常委会",
     "source": "https://www.nehe.gov.cn/nehe/c100477/redirect_firstArticle.shtml"},
    # ── 市政协 ──
    {"id": 19, "name": "梁春华", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年10月", "birthplace": "", "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "讷河市政协党组书记、主席", "current_org": "讷河市政协",
     "source": "https://www.nehe.gov.cn/nehe/c100479/202601/c02_604598.shtml"},
    {"id": 20, "name": "李晓东", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "讷河市政协副主席", "current_org": "讷河市政协",
     "source": "https://www.nehe.gov.cn/nehe/c100479/redirect_firstArticle.shtml"},
    {"id": 21, "name": "孟凡", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "讷河市政协副主席", "current_org": "讷河市政协",
     "source": "https://www.nehe.gov.cn/nehe/c100479/redirect_firstArticle.shtml"},
]

# ── POSITIONS ──────────────────────────────────────────────────────

positions = [
    # 王永平 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "中共讷河市委书记、党校校长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持市委全面工作"},
    # 栾云巍 — 市长
    {"person_id": 2, "org_id": 1, "title": "中共讷河市委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 3, "title": "讷河市人民政府市长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持市政府全面工作"},
    # 李青春 — 市委副书记
    {"person_id": 3, "org_id": 1, "title": "中共讷河市委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助市委书记抓党的建设工作"},
    {"person_id": 3, "org_id": 9, "title": "讷河市委统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼任"},
    # 唐守志 — 常委、副市长
    {"person_id": 4, "org_id": 1, "title": "中共讷河市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "讷河市政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 战伟 — 政法委书记
    {"person_id": 5, "org_id": 1, "title": "中共讷河市委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责政法、社会稳定工作"},
    # 刘宽 — 纪委书记
    {"person_id": 6, "org_id": 1, "title": "中共讷河市委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责纪检、监察、巡察工作"},
    # 王磊 — 组织部长
    {"person_id": 7, "org_id": 1, "title": "中共讷河市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责组织、干部、人才工作"},
    # 宋金英 — 宣传部长
    {"person_id": 8, "org_id": 1, "title": "中共讷河市委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责宣传思想文化工作"},
    # 徐渤程 — 常务副市长
    {"person_id": 9, "org_id": 1, "title": "中共讷河市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "讷河市政府党组副书记、副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责市政府常务工作"},
    # 董亮 — 人武部政委
    {"person_id": 10, "org_id": 10, "title": "讷河市人民武装部上校政治委员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责市人民武装部工作"},
    # 刘广伟 — 副市长
    {"person_id": 11, "org_id": 3, "title": "讷河市政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责城乡规划建设、自然资源管理"},
    # 冯雪光 — 副市长
    {"person_id": 12, "org_id": 3, "title": "讷河市政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责教育、文化体育、卫生健康"},
    # 马玉洁 — 副市长
    {"person_id": 13, "org_id": 3, "title": "讷河市政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责民政、市场监管"},
    # 李长宝 — 副市长
    {"person_id": 14, "org_id": 3, "title": "讷河市政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责农业农村、乡村振兴"},
    # 东宇辉 — 人大主任
    {"person_id": 15, "org_id": 4, "title": "讷河市人大常委会主任、党组书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持市人大常委会全面工作"},
    # 朱凤春 — 人大副主任
    {"person_id": 16, "org_id": 4, "title": "讷河市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 杨振宇 — 人大副主任
    {"person_id": 17, "org_id": 4, "title": "讷河市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 赵福元 — 人大副主任
    {"person_id": 18, "org_id": 4, "title": "讷河市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 梁春华 — 政协主席
    {"person_id": 19, "org_id": 5, "title": "讷河市政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持市政协全面工作"},
    # 李晓东 — 政协副主席
    {"person_id": 20, "org_id": 5, "title": "讷河市政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 孟凡 — 政协副主席
    {"person_id": 21, "org_id": 5, "title": "讷河市政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────

relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "讷河市委班子党政正职搭档", "overlap_org": "中共讷河市委员会/讷河市人民政府", "overlap_period": ""},
    # 书记-副书记搭档
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "讷河市委正副书记搭档", "overlap_org": "中共讷河市委员会", "overlap_period": ""},
    # 书记-政法委
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委-政法委班子搭档", "overlap_org": "中共讷河市委员会/市委政法委", "overlap_period": ""},
    # 书记-纪委
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "市委-纪委班子搭档", "overlap_org": "中共讷河市委员会/市纪委", "overlap_period": ""},
    # 书记-组织部
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "市委-组织部班子搭档", "overlap_org": "中共讷河市委员会/市委组织部", "overlap_period": ""},
    # 书记-宣传部
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "市委-宣传部班子搭档", "overlap_org": "中共讷河市委员会/市委宣传部", "overlap_period": ""},
    # 市长-常务副市长
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "市政府正副职搭档", "overlap_org": "讷河市人民政府", "overlap_period": ""},
    # 市长-副市长(唐守志)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "市政府正副职搭档", "overlap_org": "讷河市人民政府", "overlap_period": ""},
    # 市长-人大主任
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "政府-人大班子搭档", "overlap_org": "讷河市人民政府/市人大常委会", "overlap_period": ""},
    # 副书记-统战部长(兼任)
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "市委班子搭档", "overlap_org": "中共讷河市委员会", "overlap_period": ""},
    # 人大-政协
    {"person_a": 15, "person_b": 19, "type": "overlap", "context": "人大-政协班子搭档", "overlap_org": "讷河市人大常委会/讷河市政协", "overlap_period": ""},
    # 书记-人大主任
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "市委-人大班子搭档", "overlap_org": "中共讷河市委员会/市人大常委会", "overlap_period": ""},
    # 书记-政协主席
    {"person_a": 1, "person_b": 19, "type": "overlap", "context": "市委-政协班子搭档", "overlap_org": "中共讷河市委员会/讷河市政协", "overlap_period": ""},
    # 组织-宣传: 常委间部门协作
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "常委班子组织部-宣传部协作", "overlap_org": "中共讷河市委员会", "overlap_period": ""},
    # 政府副市长间
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "市政府副职搭档", "overlap_org": "讷河市人民政府", "overlap_period": ""},
    {"person_a": 13, "person_b": 14, "type": "overlap", "context": "市政府副职搭档", "overlap_org": "讷河市人民政府", "overlap_period": ""},
]

# ── BUILD ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=False,
    )
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
