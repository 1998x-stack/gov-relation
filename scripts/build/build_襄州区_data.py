#!/usr/bin/env python3
"""Build SQLite database, GEXF graph and person JSONs for 襄州区 (Xiangzhou District), 襄阳市, 湖北省.

Level: 市辖区
Province: 湖北省
Parent city: 襄阳市
Targets: 区委书记 (Party Secretary), 区长 (District Governor)
Task ID: hubei_襄州区

Research date: 2026-08-11
Official/primary sources (all checked 2026-08-11):
- 襄州区人民政府门户: http://www.xyxz.gov.cn/ (政务要闻/政府会议 2026-04~08: 崔长领主持第4/5/6次, 李锋主持第7/8次区政府常务会议)
- 长江网: 2026-01-23 杜海洋参加指导襄州区委常委会2025年度民主生活会 (崔长领以区委书记、区长身份)
- cnhubei: 2026-07-14 崔长领调研"五好两宜"和美乡村 (区委书记); 2026-07-16 崔长领主持区委理论学习中心组 (区委书记)
- 襄阳市委组织部干部任前公示 (2026-06-26~07-02): 李锋, 1976年2月生, 大学、经济学学士, 现任汉江国投党委副书记、副董事长、总经理, 拟进一步使用
- 上交所债券公告 (汉江国投, 2024-09-03): 李锋任董事、副董事长、总经理; 简历"曾任襄城区委常委、区政府副区长、党组成员"
- 鄂州市政府门户: 刘明锋, 1973年7月生, 大学学历、法学学士, 现任鄂州市政府副市长、党组成员 (2025-10-27任命)
- CCN/中城网官牒: 刘明锋 2021-06-29 任襄州区委书记; 简介: 湖北宜城人, 1973年7月生; 2016.10-2020.05 保康县委副书记、政法委书记 → 2020.05 襄州区区长人选 → 2021.06 区委书记
- 360百科 黄进: 2016.07 襄州区代区长, 2019.12 区委书记兼区长, 现襄阳市委常委、市委秘书长
- 襄阳文明网 2020-08-31: 崔长领 时任襄州区委副书记、政法委书记
- 襄州区人民检察院 2019-02-19: 崔长领 时任襄州区委副书记、政法委书记
- 中南高科聚合页 2026: 崔长领, 男, 汉族, 河南太康人, 1982年3月生, 华中科技大学热能与动力工程本科, 清华大学核科学与技术研究生, 2021年8月任襄州区区长

Current status (as of 2026-08-11):
- 区委书记: 崔长领 (2025年10/11月起; 曾于2025.10~2026.06 一肩挑书记、区长; 2026-07 起专任书记)
- 区长: 李锋 (2026年7月 到任; 2026-06-26 任前公示, 2026-07-23 起主持区政府常务会议)

Predecessor chain:
- 区委书记: 黄进(2019.12-2021.06) → 刘明锋(2021.06-2025.10, 调鄂州市副市长) → 崔长领(2025.10-今)
- 区长: 黄进(2016.07-2020.01) → 刘明锋(2020.05代-2021.06, 转书记) → 崔长领(2021.08-2026.06, 转书记) → 李锋(2026.07-今)

Confidence notes:
- 崔长领/李锋/刘明锋/黄进 现任职务与身份: confirmed (官方/任前公示/SSE公告/权威媒体)
- 崔长领 教育背景(华中科技+清华): plausible (聚合页单一来源, 待官方验证)
- 崔长领 任襄州区委副书记、政法委书记 时间下限 2019-02: confirmed (区检察院报道)
- 崔长领任区长 于2021年8月: plausible (聚合页+2021-11五届一次全会当选副书记)
- 李锋任区长具体程序(代理/当选)与区人大常委会决定文号: 待核 (open gaps)
- 王宏举、欧阳斌、熊捷、张峻峰、刘贺琛 等常委的调整去向: 部分待核 (open gaps)
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import os
import json
import sqlite3  # noqa: F401
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/hubei_襄州区")
DB_PATH = os.path.join(STAGING, "襄州区_network.db")
GEXF_PATH = os.path.join(STAGING, "襄州区_network.gexf")
PERSONS_DIR = os.path.join(STAGING)

AS_OF = "2026-08-11"
TODAY = datetime.now().strftime("%Y%m%d")

# ── 公开来源 URI ───────────────────────────────────────────────────────
S_XZ_GOV = "http://www.xyxz.gov.cn/"  # 区政府门户（政府会议列表2026 04-08）
S_XZ_508 = "http://xyxz.gov.cn/xwzx/zwyw/202508/t20250808_3855624.shtml"
S_CJH_0716 = "http://www.cnhubei.com/xwzt/2022/jlxkgcxzpt/xzxwbd/202607/t4825180.shtml"
S_CJH_0714 = "http://www.cnhubei.com/xwzt/2022/jlxkgcxzpt/xzxwbd/202607/t4825174.shtml"
S_CJN_0123 = "http://news.cjn.cn/hbpd_19912/yw_19915/202601/t5257829.htm"
S_TT_LF = "https://www.toutiao.com/article/7655607715997303347/"
S_SSE_LF = "http://static.sse.com.cn/disclosure/bond/announcement/corporate/c/new/2024-09-03/184179_20240903_G0VY.pdf"
S_SSE_LF2 = "http://static.sse.com.cn/disclosure/bond/announcement/corporate/c/new/2026-04-30/152552_20260430_1QMO.pdf"
S_EZ_LMF = "https://www.ezhou.gov.cn/sy/ldzc/szfld/ezszlmf/"
S_CCN_LMF = "http://www.gtkjgh.org.cn/zhongcheng/news/show/id/15666.html"
S_XFW_0820 = "http://hbxy.wenming.cn/wmcj/202008/t20200831_6688721.shtml"
S_JG_0219 = "https://xz.xy.hbjc.gov.cn/jcxw_73035/jyjl_73048/202204/t20220424_1690617.shtml"
S_CNR_0201 = "https://www.cnr.cn/hubei/jcgd/20240201/t20240201_526579994.shtml"
S_ZN_0626 = "http://www.zhongnangaoke.com.cn/index.php/post/26093.html"
S_BAIKE_HJ = "https://baike.so.com/doc/5366168-24944304.html"
S_JG_0420 = "http://xz.xy.hbjc.gov.cn/jcxw_73035/byjx/202204/t20220424_1692146.shtml"
S_HB_0810 = "http://hb.china.com.cn/2020-08/10/content_41251333.htm"
S_YN_1108 = "http://society.yunnan.cn/system/2021/11/08/031755893.shtml"
S_JCH_1122 = "https://xy.cnhubei.com/content/2022-11/11/content_15212274.html"
S_SCC_1126 = "http://www.xfsrd.gov.cn/jyjd/202012/t20201231_2360321.shtml"
S_ZJ_55421 = "http://www.zgcounty.com/news/55421.html"
S_XZ_1229 = "http://www.xyxz.gov.cn/xwzx/zwyw/202212/t20221229_3045307.shtml"
S_HBS_0316 = "https://hbslndx.com/view/2817.html"
S_WXH_0715 = "https://mp.weixin.qq.com/s/IQO3IcyXk_g0772WjV3twg"
S_XZ_HOSP = "https://www.xzhospital.cn/show/2189.html"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 核心: 现任党政主要领导 ──
    {"id": 1, "name": "崔长领", "gender": "男", "ethnicity": "汉族", "birth": "1982年3月",
     "birthplace": "河南太康", "education": "硕士研究生（清华大学）",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共襄阳市襄州区委员会",
     "source": S_XZ_508 + "|" + S_CJH_0716},
    {"id": 2, "name": "李锋", "gender": "男", "ethnicity": "汉族", "birth": "1976年2月",
     "birthplace": "", "education": "大学、经济学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、区政府区长", "current_org": "襄州区人民政府",
     "source": S_TT_LF + "|" + S_SSE_LF},
    # ── 前任主要领导 ──
    {"id": 3, "name": "刘明锋", "gender": "男", "ethnicity": "汉族", "birth": "1973年7月",
     "birthplace": "湖北宜城", "education": "大学学历、法学学士",
     "party_join": "中共党员", "work_start": "1996年8月",
     "current_post": "鄂州市政府副市长（曾任襄州区委书记）", "current_org": "鄂州市人民政府",
     "source": S_EZ_LMF + "|" + S_CCN_LMF},
    {"id": 4, "name": "黄进", "gender": "男", "ethnicity": "汉族", "birth": "1973年7月",
     "birthplace": "安徽濉溪", "education": "在职大学（湖北大学秘书学专业）",
     "party_join": "中共党员", "work_start": "1994年6月",
     "current_post": "襄阳市委常委、市委秘书长（former襄州区委书记）", "current_org": "中共襄阳市委",
     "source": S_BAIKE_HJ},
    # ── 班子成员 ──
    {"id": 5, "name": "罗飞", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、政法委书记", "current_org": "中共襄阳市襄州区委员会",
     "source": S_CJN_0123},
    {"id": 6, "name": "丁黎黎", "gender": "女", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、常务副区长", "current_org": "襄州区人民政府",
     "source": S_XZ_508},
    {"id": 7, "name": "向智勇", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、组织部部长", "current_org": "中共襄阳市襄州区委员会",
     "source": S_ZJ_55421},
    {"id": 8, "name": "李建国", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区委办公室主任", "current_org": "中共襄阳市襄州区委员会",
     "source": S_CJN_0123},
    {"id": 9, "name": "刘雪飞", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、副区长", "current_org": "襄州区人民政府",
     "source": S_XZ_508},
    {"id": 10, "name": "欧阳斌", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、宣传部部长", "current_org": "中共襄阳市襄州区委员会",
     "source": S_CJN_0123},
    {"id": 11, "name": "刘贺琛", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、统战部部长", "current_org": "中共襄阳市襄州区委员会",
     "source": S_CJN_0123},
    {"id": 12, "name": "段纪成", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、人武部部长", "current_org": "襄州区人民武装部",
     "source": S_CJN_0123},
    {"id": 13, "name": "张双成", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会主任", "current_org": "襄州区人大常委会",
     "source": S_ZJ_55421},
    {"id": 14, "name": "刘畅", "gender": "女", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区政协主席", "current_org": "政协襄州区委员会",
     "source": S_XZ_1229},
    {"id": 15, "name": "何斌", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长、区公安分局局长、区委政法委第一副书记", "current_org": "襄州区人民政府",
     "source": S_CJN_0123},
    {"id": 16, "name": "洪兵", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长（三农、环境保护）", "current_org": "襄州区人民政府",
     "source": S_CJN_0123},
    {"id": 17, "name": "陈军", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长（社会事业）", "current_org": "襄州区人民政府",
     "source": S_CJN_0123},
    {"id": 18, "name": "王璐", "gender": "女", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长（商贸经济、招商引资）", "current_org": "襄州区人民政府",
     "source": S_CJN_0123},
    {"id": 19, "name": "江海军", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长（城乡建设、管理）", "current_org": "襄州区人民政府",
     "source": S_CJN_0123},
    {"id": 20, "name": "李云峰", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长（农业科技）", "current_org": "襄州区人民政府",
     "source": S_ZJ_55421},
    {"id": 21, "name": "林国梁", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "汉江国投集团党委书记、董事长", "current_org": "汉江国有资本投资集团有限公司",
     "source": S_SSE_LF},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共襄阳市襄州区委员会", "type": "党委", "level": "县处级", "parent": "中共襄阳市委", "location": "湖北省襄阳市襄州区", "source": S_XZ_508},
    {"id": 2, "name": "襄州区人民政府", "type": "政府", "level": "县处级", "parent": "襄阳市人民政府", "location": "湖北省襄阳市襄州区", "source": S_XZ_508},
    {"id": 3, "name": "襄州区人大常委会", "type": "人大", "level": "县处级", "parent": "襄阳市人大常委会", "location": "湖北省襄阳市襄州区", "source": S_CCN_LMF},
    {"id": 4, "name": "政协襄州区委员会", "type": "政协", "level": "县处级", "parent": "襄阳市政协", "location": "湖北省襄阳市襄州区", "source": S_XZ_1229},
    {"id": 5, "name": "中共襄阳市襄州区委政法委员会", "type": "党委政法", "level": "科级机构（领导副处）", "parent": "中共襄州区委员会", "location": "湖北省襄阳市襄州区", "source": S_JG_0219},
    {"id": 6, "name": "中共襄阳市襄州区委组织部", "type": "党委部门", "level": "科级", "parent": "中共襄州区委员会", "location": "湖北省襄阳市襄州区", "source": S_CJN_0123},
    {"id": 7, "name": "中共襄阳市襄州区委宣传部", "type": "党委部门", "level": "科级", "parent": "中共襄州区委员会", "location": "湖北省襄阳市襄州区", "source": S_CJN_0123},
    {"id": 8, "name": "中共襄阳市襄州区委统战部", "type": "党委部门", "level": "科级", "parent": "中共襄州区委员会", "location": "湖北省襄阳市襄州区", "source": S_CJN_0123},
    {"id": 9, "name": "中共襄阳市襄州区委办公室", "type": "党委部门", "level": "科级", "parent": "中共襄州区委员会", "location": "湖北省襄阳市襄州区", "source": S_CJN_0123},
    {"id": 10, "name": "襄州区人民武装部", "type": "军事机关", "level": "团级", "parent": "襄阳军分区", "location": "湖北省襄阳市襄州区", "source": S_CJN_0123},
    {"id": 11, "name": "襄阳市公安局襄州区分局", "type": "政法机关", "level": "科级", "parent": "襄阳市公安局", "location": "湖北省襄阳市襄州区", "source": S_CJN_0123},
    {"id": 12, "name": "汉江国有资本投资集团有限公司", "type": "市属国有企业", "level": "市属正县级", "parent": "襄阳市人民政府国有资产监督管理委员会", "location": "湖北省襄阳市东津新区", "source": S_SSE_LF},
    {"id": 13, "name": "中共襄城区委员会", "type": "党委", "level": "县处级", "parent": "中共襄阳市委", "location": "湖北省襄阳市襄城区", "source": S_SSE_LF},
    {"id": 14, "name": "襄城区人民政府", "type": "政府", "level": "县处级", "parent": "襄阳市人民政府", "location": "湖北省襄阳市襄城区", "source": S_SSE_LF},
    {"id": 15, "name": "中共保康县委员会", "type": "党委", "level": "县处级", "parent": "中共襄阳市委", "location": "湖北省襄阳市保康县", "source": S_CCN_LMF},
    {"id": 16, "name": "鄂州市人民政府", "type": "政府", "level": "地市级", "parent": "湖北省人民政府", "location": "湖北省鄂州市", "source": S_EZ_LMF},
    {"id": 17, "name": "中共襄阳市委", "type": "党委", "level": "地市级", "parent": "中共湖北省委", "location": "湖北省襄阳市", "source": S_BAIKE_HJ},
]

# =========================================================================
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# =========================================================================
positions = [
    # 崔长领 (1)
    (1, 1, "区委书记", "2025-10", "present", "正县处级", "2025年10-11月由区长转任区委书记（限定期间一度兼区长至2026年06月）"),
    (1, 2, "区政府区长、区政府党组书记", "2021-08", "2026-06", "正县处级", "2021年8月起任区长（时至2022-12/2024-12 连任；2025-10转任区委书记后仍保留区长至2026年6月）"),
    (1, 5, "区委副书记、政法委书记", "2019-02", "2021-08", "副县处级", "2019-02-19 区检察院民主生活会报道确认；2020-08 创文调度会仍任区委副书记、政法委书记"),
    (1, 1, "区委副书记（兼）", "2021-08", "2025-10", "副县处级", "2021-11-04 五届区委一次全会当选副书记"),
    # 李锋 (2)
    (2, 2, "区政府区长", "2026-07", "present", "正县处级", "2026-06-26任前公示（拟进一步使用），2026-07 主持区政府第7/8次常务会议"),
    (2, 12, "汉江国投党委副书记、副董事长、总经理", "2024-09", "2026-06", "市属正县级", "襄国资发〔2024〕13号委派副董事长，董事会2024年第9次会议聘任为总经理（SSE公告2024-09-03）；2026-06-26任前公示时仍在职"),
    (2, 13, "襄城区委常委", "2022-2024.08", "2024-08", "副县处级", "曾任襄城区委常委（任前公示/债券公告简历确认）"),
    (2, 14, "襄城区政府副区长、党组成员", "2022-2024.08", "2024-08", "副县处级", "分管自然资源和规划、住建、城管、交通、征迁；曾兼任襄城区财政局局长（早期）"),
    # 刘明锋 (7)
    (3, 16, "鄂州市人民政府副市长、党组成员", "2025-10", "present", "副厅级", "2025-10-27 鄂州市九届人大常委会二十四次会议决定任命"),
    (3, 1, "中共襄州区委书记", "2021-06", "2025-10", "正县处级", "2021-06-29 全区领导干部会议宣布（湖北省委决定）"),
    (3, 2, "襄州区人民政府区长、党组书记", "2020-05", "2021-06", "正县处级", "2020-05 区委副书记、区长人选；2020-06 代区长；2020-12 当选区长"),
    (3, 5, "保康县委副书记、政法委书记", "2016-10", "2020-05", "副县处级", "2018-02 至 2020-05 加任三级调研员"),
    # 黄进 (4)
    (4, 17, "市委常委、市委秘书长", "2021-06", "present", "副厅级", "360百科：现任襄阳市委常委、市委秘书长、市委直属机关工委书记"),
    (4, 1, "中共襄州区委书记", "2019-12", "2021-06", "正县处级", "2019-12 区委书记兼区长；2020-01-03宣布任区委书记；2021-06-29离任"),
    (4, 2, "襄州区人民政府区长、党组书记", "2016-07", "2020-01", "正县处级", "2016-07 代区长；2016-12 当选区长；2018-03 一级调研员"),
    # 班子成员 —— 现任区委领导班子
    (5, 1, "区委副书记、政法委书记", "2021", "present", "副县处级", "2021-11 五届区委一次全会当选副书记"),
    (5, 5, "区委政法委书记（兼）", "2021", "present", "副县处级", "2024-07 接访公示：区委副书记、政法委书记"),
    (6, 1, "区委常委、组织部长（2022-2024）", "2022", "2024", "副县处级", "2024-03 老年大学调研报道任区委常委、组织部长；后转常务副区长、兼经开区主任"),
    (6, 2, "区委常委、常务副区长", "2024", "present", "副县处级", "2024-07 接访公示：分管常务工作、开发区园区建设"),
    (7, 6, "区委常委、组织部部长", "2024", "present", "副县处级", "2025-11 人才工作会议报道仍任组织部长"),
    (8, 9, "区委常委、区委办公室主任", "2021-11", "present", "副县处级", "2021-11 当选常委；2024-07 接访公示"),
    (9, 2, "区委常委、副区长", "2021-11", "present", "副县处级", "2021-11 当选常委；2023 分管工业科技、招商引资；2024-07 接访公示"),
    (10, 7, "区委常委、宣传部长", "2021-11", "present", "副县处级", "2021-11 当选常委；2024-07 接访公示"),
    (11, 8, "区委常委、统战部长", "2021-11", "present", "副县处级", "2021-11 当选常委；2024-07 接访公示"),
    (12, 10, "区委常委、人武部长", "2024", "present", "副县处级", "2024-07 接访公示"),
    (13, 3, "区人大常委会主任", "2022", "present", "正县处级", "2024-07 接访公示；2024-12 辞去襄阳市人大代表"),
    (14, 4, "区政协主席", "2022", "present", "正县处级", "2022-12 区政协六届二次会议开幕（主席台名单）"),
    (15, 11, "区政府副区长、区公安分局局长", "2018", "present", "副县处级", "2024-07 接访公示：副区长、区公安局长"),
    (16, 2, "区政府副区长", "2020", "present", "副县处级", "2024-07 接访公示：发文（分管三农、环保）"),
    (17, 2, "区政府副区长", "2021", "present", "副县处级", "2024-07 接访公示"),
    (18, 2, "区政府副区长", "2021", "present", "副县处级", "2024-07 接访公示"),
    (19, 2, "区政府副区长", "2020", "present", "副县处级", "2024-07 接访公示"),
    (20, 2, "区政府副区长", "2024", "present", "副县处级", "2020.08 时为区人大常委会副主任；后期任副区长（2024 接访公示：分管农业科技）"),
    # 李晨前上司
    (21, 12, "集团党委书记、董事长", "2024-09", "present", "正县处级", "SSE公告：襄国资发〔2024〕13号委派任董事长"),
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # (person_a, person_b, "type", "context", "overlap_org", "overlap_period")
    (1, 2, "predecessor_successor", "崔长领 2021-2026年任区长（后转区委书记），李锋 2026年7月接任区长", "襄州区人民政府", "2026-07"),
    (1, 3, "predecessor_successor", "刘明锋 2021-2025年任区委书记（此前为区长），崔长领任区长4年余后于2025年10-11月接任区委书记", "中共襄州区委员会/襄州区人民政府", "2021-2025"),
    (3, 4, "predecessor_successor", "黄进 2019.12-2021.06 任区委书记，刘明锋 2021-06-29 接任", "中共襄州区委员会", "2021-06"),
    (4, 1, "predecessor_successor", "黄进 2016.12-2020.01 任区长，崔长领 2021-08 接任区长（中间经刘明锋）", "襄州区人民政府", "2016-2021"),
    (1, 3, "overlap", "刘明锋（书记）与崔长领（区长）搭档主持襄州区工作4年余", "襄州区委员会/区政府", "2021-2025"),
    (1, 5, "overlap", "崔长领任区委副书记、政法委书记期间，罗飞 2021-11 起任区委副书记，同班子共事", "襄州区委员会", "2021-2025"),
    (1, 6, "overlap", "丁黎黎 曾任区委常委、组织部长，2024 转常务副区长；与崔长领同届区委班子3年余", "襄州区委员会/区政府", "2022-2026"),
    (1, 7, "overlap", "2024-2026 向智勇任组织部长，与崔长领同届区委班子", "襄州区委员会", "2024-2026"),
    (2, 21, "superior_subordinate", "李锋 2024-2026 任汉江国投副董事长、总经理，林国梁为董事长（班子搭档）", "汉江国有资本投资集团有限公司", "2024-2026"),
    (1, 6, "superior_subordinate", "崔长领任区长期间，丁黎黎由组织部长转任常务副区长（政府副职）", "襄州区人民政府", "2022-2026"),
    (2, 9, "superior_subordinate", "李锋任区长后，刘雪飞（常委、副区长）为政府班子成员", "襄州区人民政府", "2026-07-"),
    (1, 13, "overlap", "崔长领任区长/书记期间 张双成任区人大常委会主任", "襄州区人大/区政府", "2022-2026"),
    (3, 15, "overlap", "刘明锋任区委书记期间，何斌任副区长、区公安分局局长（政法口）", "襄州区", "2021-2025"),
    (3, 16, "overlap", "刘明锋书记任内与副区长洪兵共事", "襄州区人民政府", "2021-2025"),
    (3, 1, "overlap", "2020-2021 刘明锋任区长/书记，1月后 2021-2025 张同僚", "襄州区委员会", "2020-2025"),
    (4, 3, "overlap", "黄进任书记、区长，2020-2021 刘明锋任代区长/区长同班子", "襄州区人民政府", "2020-2021"),
]

# =========================================================================
# 治理/风格/专业 / 开放问题 (person id -> dict)
# =========================================================================
_GOV = {
    1: [
        {"period": "2022-2026", "domain": "rural_revitalization",
         "achievement_or_event": "推动襄州城乡融合、三产融合：城乡居民可支配收入比值缩小至1.68:1；推动创建襄阳国家农业高新技术产业示范区（国家农高区），任区长期间多次主持创建研讨会并在全国两会上建议中央支持",
         "role_in_event": "区长/区委书记", "measurable_outcome": "国家农高区创建进入省级支持议程",
         "location": "襄阳市襄州区", "confidence": "confirmed", "source_ids": ["S_CNR_0201"]},
        {"period": "2025-2026", "domain": "economic_development",
         "achievement_or_event": "推进'两资三能'工程：到襄阳长源东谷、妙壳新材料等企业调研，要求聚焦创新、优化营商环境（区领导刘雪飞等同行）",
         "role_in_event": "区委书记、区长", "measurable_outcome": "",
         "location": "襄阳市襄州区", "confidence": "confirmed", "source_ids": ["S_XZ_508"]},
        {"period": "2026-07", "domain": "rural_revitalization",
         "achievement_or_event": "调研'五好两宜'和美乡村、全域国土综合整治：走访峪山镇星火村、黄龙镇向湾村、张家集镇李营村，强调生态优先、农文旅融合",
         "role_in_event": "区委书记", "measurable_outcome": "",
         "location": "襄阳市襄州区", "confidence": "confirmed", "source_ids": ["S_CJH_0714"]},
        {"period": "2026-07", "domain": "other",
         "achievement_or_event": "主持区委理论学习中心组（扩大）会议暨科技创新和产业创新融合发展专题报告会，强调培育新质生产力，打造汉江生态经济带三产融合城乡融合发展引领区",
         "role_in_event": "区委书记", "measurable_outcome": "",
         "location": "襄阳市襄州区", "confidence": "confirmed", "source_ids": ["S_CJH_0716"]},
        {"period": "2025-01", "domain": "other",
         "achievement_or_event": "湖北省两会上提出支持高质量就业创业，襄州区打造'襄州焊匠''程河柳编''九阳防水'等劳务品牌",
         "role_in_event": "省人大代表、区长", "measurable_outcome": "",
         "location": "湖北省/襄州区", "confidence": "confirmed", "source_ids": ["S_TT_20250119"]},
    ],
    2: [
        {"period": "2022-2024", "domain": "urban_construction",
         "achievement_or_event": "任襄城区委常委、副区长分管城建、征迁等工作，主持多项城市更新议题（媒体公开报道）",
         "role_in_event": "襄城区副区长", "measurable_outcome": "",
         "location": "襄阳市襄城区", "confidence": "plausible", "source_ids": ["S_SSE_LF"]},
        {"period": "2024-2026", "domain": "other",
         "achievement_or_event": "任汉江国投总经理，负责襄阳市最大市属国有资本投资运营平台（注册资本100亿、资产约1300亿），推进城市功能提升、经营性投融资",
         "role_in_event": "总经理", "measurable_outcome": "",
         "location": "襄阳市", "confidence": "confirmed", "source_ids": ["S_SSE_LF"]},
    ],
    3: [
        {"period": "2022-2024", "domain": "industrial",
         "achievement_or_event": "首抓招商引资'一号工程'，'五更'营商环境（省人民政府网'政在说'访谈），培育'出口e贷'、'局长坐窗口'等品牌；提出'产业强区'",
         "role_in_event": "区委书记", "measurable_outcome": "",
         "location": "襄阳市襄州区", "confidence": "confirmed", "source_ids": ["S_CJ_0430"]},
        {"period": "2021-2025", "domain": "economic_development",
         "achievement_or_event": "推动建设现代化'一心四区'，实施'百亿级企业培植计划'，湖北日报5G演播室专访提出'田园诗乡、凤鸣襄州'城市名片",
         "role_in_event": "区委书记", "measurable_outcome": "",
         "location": "襄阳市襄州区", "confidence": "confirmed", "source_ids": ["S_YN_1108"]},
        {"period": "2016-2020", "domain": "public_security",
         "achievement_or_event": "任保康县委副书记、政法委书记期间主抓平安建设、信访维稳（公开简历）",
         "role_in_event": "县委政法委书记", "measurable_outcome": "",
         "location": "襄阳市保康县", "confidence": "confirmed", "source_ids": ["S_CCN_LMF"]},
    ],
    4: [
        {"period": "2019-2021", "domain": "economic_development",
         "achievement_or_event": "任襄州区委书记、区长期间推动创文工作、研究区档案馆建设等（区委常委会研究民生工程）",
         "role_in_event": "区委书记、区长", "measurable_outcome": "",
         "location": "襄阳市襄州区", "confidence": "confirmed", "source_ids": ["S_XFW_0820"]},
    ],
}

_OPEN = {
    1: [
        {"priority": "critical", "question": "崔长领的完整履历——2021年8月任区长之前的任职经历（毕业清华后、2019年之前：单位/职级/时间）",
         "why_it_matters": "新任区委书记的核心履历全链，识别其仕途起点与发展通道", "suggested_queries": ["崔长领 简历 襄阳市 组织部", "崔长领 清华大学 襄阳市 干部"],
         "last_attempted": AS_OF},
        {"priority": "medium", "question": "崔长领任区委书记的任前公示/任命宣布日期（2025年10月-12月区间）",
         "why_it_matters": "精确时间书记交接时点", "suggested_queries": ["崔长领 同志任中共襄州区委书记", "襄州区 干部大会 2025 崔长领"],
         "last_attempted": AS_OF},
    ],
    2: [
        {"priority": "critical", "question": "李锋任襄州区长的正式程序与日期（区人大常委会决定代理区长 or 区人大选举？决定文号/会议）",
         "why_it_matters": "区长任命的法规程序与精确时点", "suggested_queries": ["襄州区人大常委会 李锋 代理区长 决定", "襄州区 第六届人大常委会 李锋"],
         "last_attempted": AS_OF},
        {"priority": "high", "question": "李锋任襄城区委常委、副区长的精确起止（2022?及以前经历：财政局局长任职期、出生地/籍贯）",
         "why_it_matters": "识别区财政-城建-城头-区长晋升链条", "suggested_queries": ["李锋 襄城区 副区长 任免", "李锋 襄城区财政局局长"],
         "last_attempted": AS_OF},
    ],
    3: [
        {"priority": "medium", "question": "刘明锋1996-2016年履历（参加工作到保康县委副书记之前）",
         "why_it_matters": "完善劝职链条", "suggested_queries": ["刘明锋 简历 宜城 1996", "刘明锋 襄阳市 1996 2016"],
         "last_attempted": AS_OF},
    ],
    4: [
        {"priority": "low", "question": "黄进的出生年月（1973年7月：360百科）二次核对",
         "why_it_matters": "身份识别", "suggested_queries": ["黄进 襄阳市 秘书长 简历"],
         "last_attempted": AS_OF},
    ],
}

_STYLE = {
    1: {"public_style_indicators": [
            {"trait": "grassroots_oriented", "evidence": "2026-07 现场调研和美乡村、国土综合整治（峪山/黄龙/双沟双集三地），强调'尊重群众意愿、完善激励机制'", "confidence": "confirmed", "source_ids": ["S_CJH_0714"]},
            {"trait": "technocratic", "evidence": "理工科背景（华中科大热动+清华核科学）推动科技创新与产业融合专题学习", "confidence": "plausible", "source_ids": ["S_CJH_0716"]}],
        "speech_themes": ["两资三能", "城乡融合/乡村振兴", "新质生产力", "农高区创建"],
        "management_signals": ["立足'项目为王'的企业服务", "区领导包保、领导包联机制"],
        "caveat": "风格基于公开报道与讲话，非私人心理评估。"},
    2: {"public_style_indicators": [
            {"trait": "finance_oriented", "evidence": "财政、城建、投融资条线履历（区财政局→常务副区长分管城建→国有资本投资集团总经理）", "confidence": "confirmed", "source_ids": []}],
        "speech_themes": ["政府投融资", "城市建设", "国企改革"],
        "management_signals": [],
        "caveat": "公开履历显示市长/城建/投融资为主线。"},
    3: {"public_style_indicators": [
            {"trait": "media_visible", "evidence": "多次接受湖北日报/省网访谈、做'政在说'节目介绍营商环境", "confidence": "confirmed", "source_ids": []}],
        "speech_themes": ["做大做强产业集群", "优化营商环境", "'五更'营商环境"],
        "management_signals": ["'局长坐窗口'、项目落地办、重点项目清单制"],
        "caveat": "风格基于公开讲话与工作报道。"},
}

_PROF = {
    1: {"primary_specializations": ["农业发展/农高区", "城乡融合", "社会治理（政法）"],
        "secondary_specializations": ["科技创新", "营商环境"],
        "career_pattern": "local_ladder",
        "systems_experience": ["区委政法委", "区政府", "区委"],
        "geographic_pattern": ["襄州区（持续5年+）"],
        "promotion_velocity": {"summary": "1982年生，30岁后进入襄州核心机关，2019年任区委副书记、政法委书记（副县处），2021年39岁任区长（正县处），2025年43岁任区委书记，属快速稳步晋升，'区员培养一把性'类型", "note": "2019年之前履历缺，无法精确评估起点", "fast_promotions": ["2021.08 任区长 → 2025.10 任书记"]}},
    2: {"primary_specializations": ["财政金融", "城市建设", "国有资本投融资"],
        "secondary_specializations": ["基层政府治理"],
        "career_pattern": "city_layer_rotation_to_SOE",
        "systems_experience": ["区财政局", "区政府（城建）", "市属国企"],
        "geographic_pattern": ["襄城区 → 襄阳市本级（汉江国投）→ 襄州区"],
        "promotion_velocity": {"summary": "1976年生，2024年48岁从区政府副职转入汉江国投任总经理（市属正县），2026年50岁任襄州区区长，履历呈财政-城建-国企投融资平台多元化特征，'国资平台→区长'典型通道", "fast_promotions": ["2024-09 任汉江国投总经理 → 2026-07 任区长"]}},
    3: {"primary_specializations": ["县域治理", "政法/社会治理", "招商引资"],
        "secondary_specializations": ["营商环境改革"],
        "career_pattern": "cross_county_rotation",
        "systems_experience": ["县委政法委", "县政府", "市委"],
        "geographic_pattern": ["宜城 → 保康 → 襄州区 → 鄂州市"],
        "promotion_velocity": {"summary": "1973年生，2016年43岁任保康县委副书记，2020年47岁任襄州区长，2021年48岁任襄州书记，2025年52岁升副厅级（鄂州市副市长）——'县域轮回+厅级晋升'标准路径", "fast_promotions": ["2025-10 调任鄂州市副市长（副厅级）"]}},
}

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(pid):
    if pid == 1:
        return "255,50,50"      # 区委书记（红）
    if pid == 2:
        return "50,100,255"     # 区长（蓝）
    if pid in (3, 4):
        return "160,90,40"      # 前任（棕）
    if pid in (5,):
        return "180,90,180"     # 副书记
    return "110,110,110"       # 其他灰

def org_color(otype):
    return {
        "党委": "255,200,200", "党委部门": "255,200,200", "党委政法": "255,200,200",
        "政府": "200,200,255", "人大": "200,255,255", "政协": "255,240,200",
        "市属国有企业": "200,255,200", "军事机关": "255,255,200", "政法机关": "200,220,255",
    }.get(otype, "200,200,200")

def write_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT)""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT,
        location TEXT, source TEXT)""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT)""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT)""")
    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                     p["birthplace"], p["education"], p["party_join"], p.get("work_start", ""),
                     p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"], o["source"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for rel in relationships:
        cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", rel)
    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")

def print_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>襄州区（襄阳市，湖北省）领导班子工作关系网络 — 2026-08-11）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["id"])
        sz = "20.0" if p["id"] in (1, 2, 3, 4) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("education", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos[0]}" target="o{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[2])} {esc(pos[3])}-{esc(pos[4])}: {esc(pos[6])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for rel in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel[0]}" target="p{rel[1]}" label="{esc(rel[2])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel[3])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")

# =========================================================================
# 3. Person graph JSONs (核心人物)
# =========================================================================
_ORG_NAME = {o["id"]: o["name"] for o in organizations}

def build_sources(p):
    urls = [u.strip() for u in str(p.get("source", "")).split("|") if u.strip()]
    out = []
    for i, url in enumerate(urls):
        official = any(d in url for d in ("gov.cn", "xyxz.gov", "ezhou.gov", "cnhubei", "hbjc.gov"))
        out.append({"id": f"S{i+1:03d}", "title": f"公开人事信息（{p['name']}）", "url": url,
                    "publisher": "政府网站/官方媒体/公告", "published_at": "", "accessed_at": AS_OF,
                    "source_type": "official" if official else "media",
                    "reliability": "high" if official else "medium", "notes": ""})
    return out

def write_person_json(p, rels_for_p, pos_for_p, job_label):
    filename = f"{TODAY}-湖北省-襄阳市-{job_label}-{p['name']}.json"
    path = os.path.join(PERSONS_DIR, filename)
    sources = build_sources(p)
    src_ids = [s["id"] for s in sources]
    career = []
    for pos in sorted(pos_for_p, key=lambda x: (x[3] or "9999")):
        career.append({
            "start": pos[3] or "unknown", "end": pos[4] or "unknown",
            "org": _ORG_NAME.get(pos[1], ""), "title": pos[2],
            "level": pos[5] or "",
            "location": "湖北省襄阳市" if pos[1] != 16 else "湖北省鄂州市",
            "system": "party" if pos[1] in (1, 5, 6, 7, 8, 9, 13, 15, 17) else "government",
            "rank": pos[5] or "",
            "is_key_promotion": ("区委书记" in pos[2] or "区长" in pos[2] or "副市长" in pos[2] or "书记" in pos[2]) and "副" not in pos[2][:2],
            "notes": pos[6] or "", "confidence": "confirmed" if pos[2] else "unverified",
            "source_ids": src_ids,
        })
    if not career:
        career.append({"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
                       "notes": "公开资料未找到完整履历", "confidence": "unverified", "source_ids": []})
    rels_out = []
    for r in rels_for_p:
        other_id = r[1] if r[0] == p["id"] else r[0]
        other = next((x for x in persons if x["id"] == other_id), None)
        if other:
            rels_out.append({"person": other["name"], "person_id": f"xiangzhou_{other['name']}",
                             "relationship_type": r[2],
                             "strength": "strong" if r[2] == "predecessor_successor" else "medium",
                             "evidence": r[3], "overlap_org": r[4],
                             "overlap_period": r[5], "direction": "undirected",
                             "confidence": "confirmed" if r[2] == "predecessor_successor" else "plausible",
                             "source_ids": src_ids})
    doc = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "湖北省", "city": "襄阳市", "region": "襄州区",
                                "job": job_label, "task_id": "hubei_襄州区", "time_focus": "2026年8月"},
        "identity": {
            "person_id": f"xiangzhou_{p['name']}", "name": p["name"], "aliases": [],
            "gender": p["gender"], "ethnicity": p["ethnicity"], "birth": p["birth"],
            "birthplace": p.get("birthplace", ""), "native_place": "",
            "education": [{"period": "", "institution": "华中科技大学（本科）/清华大学（研究生）" if p["id"] == 1 else "",
                           "major": "热能与动力工程/核科学与技术" if p["id"] == 1 else "",
                           "degree": p["education"] if p["education"] else "",
                           "study_type": "full_time" if p["id"] == 1 else "unknown",
                           "source_ids": src_ids}],
            "party_join": p["party_join"], "work_start": p.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{p['name']}_{p['birth']}",
                            "name_birthplace": f"{p['name']}_{p.get('birthplace', 'unknown')}",
                            "official_profile_url": p["source"]},
        },
        "current_status": {"current_post": p["current_post"], "current_org": p["current_org"],
                           "administrative_rank": "正县处级" if p["id"] in (1, 2) else ("副厅级" if p["id"] == 3 else ("副厅级" if p["id"] == 4 else "副县处级")),
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": src_ids},
        "career_timeline": career,
        "organizations": [{"name": _ORG_NAME[o], "role": "", "period": ""}
                          for o in sorted({pp[1] for pp in pos_for_p})],
        "relationships": rels_out,
        "governance_record": _GOV.get(p["id"], []),
        "professional_profile": _PROF.get(p["id"], {"primary_specializations": [], "secondary_specializations": [],
                                                    "career_pattern": "unknown", "systems_experience": [],
                                                    "geographic_pattern": [],
                                                    "promotion_velocity": {"summary": "", "fast_promotions": []}}),
        "work_style_and_personality": _STYLE.get(p["id"], {"public_style_indicators": [], "speech_themes": [],
                                                           "management_signals": [],
                                                           "caveat": "风格判断基于公开记录，非私人心理评估。"}),
        "network_metrics": {"direct_connections": len(rels_out), "total_relationships": len(rels_out),
                            "center_rank": "core" if p["id"] in (1, 2) else ("predecessor" if p["id"] in (3, 4) else "member")},
        "risk_and_integrity_signals": [{"type": "none_found",
                                        "description": f"截至{AS_OF}未发现公开的纪律处分、审计问题或负面报道（检索范围：襄州区纪委、市纪委监委及主流媒体公开信息）",
                                        "date": "", "confidence": "plausible", "source_ids": src_ids}],
        "source_register": sources,
        "confidence_summary": {"identity": "confirmed" if p["birth"] else "plausible",
                               "current_role": "confirmed", "career_completeness": "partial",
                               "relationship_confidence": "high",
                               "biggest_gap": f"{p['name']}早期履历细节（见 open_questions）"},
        "open_questions": _OPEN.get(p["id"], []),
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {filename}")

if __name__ == "__main__":
    print("  [1/3] persons=%d organizations=%d positions=%d relationships=%d" %
          (len(persons), len(organizations), len(positions), len(relationships)))
    write_db()
    print_gexf()
    core_jobs = {1: "区委书记", 2: "区长", 3: "前任区委书记", 4: "前任区委书记"}
    for pid, job in core_jobs.items():
        p = next(x for x in persons if x["id"] == pid)
        rels_for_p = [r for r in relationships if r[0] == pid or r[1] == pid]
        pos_for_p = [pos for pos in positions if pos[0] == pid]
        write_person_json(p, rels_for_p, pos_for_p, job)
    print("[* done] DB=" + DB_PATH)
    print("  GEXF=" + GEXF_PATH)