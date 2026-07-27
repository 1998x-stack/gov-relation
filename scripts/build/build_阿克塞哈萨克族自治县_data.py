"""
Build SQLite database + GEXF graph for 阿克塞哈萨克族自治县 (Aksai Kazak Autonomous County)
under 酒泉市, 甘肃省.

Current party secretary: 张桐 (since ~2026-01)
Current county chief: 库美斯剑 (since ~2021)

Data sources:
  - 阿克塞县人民政府官网 (www.akesai.gov.cn)
  - Baidu Baike entries for officials
  - 酒泉市委组织部 任前公示
  - News reports (澎湃新闻, 汲古新知, 酒泉日报)
  - 甘肃省纪委监委通报
"""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Person ID mapping ─────────────────────────────────────────────────
PID = {
    "zhang_tong": 1,
    "kumeisijian": 2,
    "tao_tao": 3,
    "zhang_peng": 4,
    "han_hu": 5,
    "feng_huichang": 6,
    "xuelian": 7,
    "yang_guoping": 8,
    "bayihazi": 9,
    "lu_baojian": 10,
    "halibieke": 11,
    "yin_yan": 12,
    "zhang_jian": 13,
    "wu_hailong": 14,
    "meng_junzheng": 15,
    "bai_zhenlin": 16,
    "mao_xuewen": 17,
}


def pid(name: str) -> int:
    return PID[name]


# ── Persons ───────────────────────────────────────────────────────────
persons = [
    dict(id=pid("zhang_tong"), name="张桐", gender="男", ethnicity="汉族",
         birth="1976-09", birthplace="甘肃（待确认）",
         education="在职大学学历，军事学学士",
         party_join="", work_start="",
         current_post="阿克塞哈萨克族自治县委书记、县人武部党委第一书记",
         current_org="中共阿克塞哈萨克族自治县委",
         source="akesai.gov.cn; baike.baidu.com; 甘肃省委组织部任前公示 (2026-01-04)"),

    dict(id=pid("kumeisijian"), name="库美斯剑", gender="女", ethnicity="哈萨克族",
         birth="1980-04", birthplace="甘肃阿克塞（推测）",
         education="在职大学学历（兰州大学行政管理专业），省委党校在职研究生",
         party_join="", work_start="",
         current_post="阿克塞哈萨克族自治县委副书记、县人民政府党组书记、县长",
         current_org="阿克塞哈萨克族自治县人民政府",
         source="akesai.gov.cn; baike.baidu.com; 阿克塞县政府官网新闻"),

    dict(id=pid("tao_tao"), name="陶涛", gender="男", ethnicity="汉族",
         birth="1973-11", birthplace="甘肃（待确认）",
         education="大学学历，农业推广硕士",
         party_join="", work_start="",
         current_post="酒泉市人民政府党组成员、副市长",
         current_org="酒泉市人民政府",
         source="baike.baidu.com; 酒泉市五届人大六次会议 (2026-01-15)"),

    dict(id=pid("zhang_peng"), name="张鹏", gender="男", ethnicity="汉族",
         birth="1980-02", birthplace="甘肃（待确认）",
         education="甘肃政法学院本科学历（法学学士），燕山大学研究生学历（公共管理硕士）",
         party_join="", work_start="2005",
         current_post="阿克塞哈萨克族自治县委副书记、县人民政府党组副书记",
         current_org="中共阿克塞哈萨克族自治县委",
         source="阿克塞县人民政府官网; 阿克塞发布公众号 (2024-04-27); 汲古新知报道"),

    dict(id=pid("han_hu"), name="韩虎", gender="男", ethnicity="汉族",
         birth="1975-08", birthplace="",
         education="在职大学学历（中央党校经济管理学专业）",
         party_join="", work_start="",
         current_post="阿克塞哈萨克族自治县委常委、县纪委书记、县监委主任",
         current_org="中共阿克塞哈萨克族自治县纪律检查委员会",
         source="阿克塞县人民政府官网（领导之窗，2023-11-30更新）"),

    dict(id=pid("feng_huichang"), name="冯辉昌", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="", party_join="", work_start="",
         current_post="阿克塞哈萨克族自治县人大常委会主任",
         current_org="阿克塞哈萨克族自治县人大常委会",
         source="阿克塞县政府官网会议报道"),

    dict(id=pid("xuelian"), name="雪莲", gender="女", ethnicity="哈萨克族（推测）",
         birth="", birthplace="",
         education="", party_join="", work_start="",
         current_post="阿克塞哈萨克族自治县政协主席",
         current_org="中国人民政治协商会议阿克塞哈萨克族自治县委员会",
         source="阿克塞县政府官网会议报道"),

    dict(id=pid("yang_guoping"), name="杨国平", gender="男", ethnicity="汉族",
         birth="1975-10", birthplace="",
         education="西北师范大学，本科",
         party_join="", work_start="",
         current_post="阿克塞哈萨克族自治县人民政府副县长",
         current_org="阿克塞哈萨克族自治县人民政府",
         source="阿克塞县人民政府官网"),

    dict(id=pid("bayihazi"), name="巴依哈孜", gender="男", ethnicity="哈萨克族",
         birth="1986-01", birthplace="",
         education="甘肃警察职业学院大专学历，省委党校研究生学历",
         party_join="", work_start="",
         current_post="阿克塞哈萨克族自治县人民政府副县长（分管农牧、乡村振兴）",
         current_org="阿克塞哈萨克族自治县人民政府",
         source="阿克塞县人民政府官网"),

    dict(id=pid("lu_baojian"), name="卢保健", gender="男", ethnicity="汉族",
         birth="1987-03", birthplace="",
         education="武汉科技大学，本科工学学士",
         party_join="", work_start="",
         current_post="阿克塞哈萨克族自治县人民政府副县长",
         current_org="阿克塞哈萨克族自治县人民政府",
         source="阿克塞县人民政府官网; 2025-05-27任命报道"),

    dict(id=pid("halibieke"), name="哈里别克", gender="男", ethnicity="哈萨克族",
         birth="", birthplace="",
         education="", party_join="", work_start="",
         current_post="酒泉市人民政府副市长（推测）",
         current_org="酒泉市人民政府",
         source="搜狐新闻报道 (2021-05); 酒泉市政府官网"),

    dict(id=pid("yin_yan"), name="银雁", gender="男", ethnicity="哈萨克族",
         birth="1966", birthplace="新疆巴里坤",
         education="", party_join="", work_start="",
         current_post="（被调查）", current_org="",
         source="酒泉市纪委监委通报 (2025-08-11); 网易新闻/北青政知新媒体"),

    dict(id=pid("zhang_jian"), name="张健", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="", party_join="", work_start="",
         current_post="阿克塞哈萨克族自治县委常委、宣传部部长",
         current_org="中共阿克塞哈萨克族自治县委宣传部",
         source="汲古新知报道 (2024-04-28); 肃州区→阿克塞县调任公示"),

    dict(id=pid("wu_hailong"), name="武海龙", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="", party_join="", work_start="",
         current_post="阿克塞哈萨克族自治县人民政府副县长、县公安局局长",
         current_org="阿克塞哈萨克族自治县公安局",
         source="汲古新知报道 (2024-01-13); 酒泉市县处级干部履新报道"),

    dict(id=pid("meng_junzheng"), name="孟军政", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="", party_join="", work_start="",
         current_post="敦煌市人民政府副市长、市公安局局长",
         current_org="敦煌市人民政府",
         source="汲古新知报道; 酒泉市县处级干部履新 (2024-01-13)"),

    dict(id=pid("bai_zhenlin"), name="白振林", gender="男", ethnicity="汉族",
         birth="1975-06", birthplace="",
         education="省委党校大学学历",
         party_join="", work_start="",
         current_post="（已调任市属国有企业正职）", current_org="",
         source="酒泉市委组织部任前公示 (2024-04)"),

    dict(id=pid("mao_xuewen"), name="毛学文", gender="男", ethnicity="汉族",
         birth="1970-11", birthplace="",
         education="在职大学学历",
         party_join="", work_start="",
         current_post="（拟任县（市、区）党委副书记）", current_org="",
         source="酒泉市委组织部任前公示 (2024-04)"),
]

# ── Organizations ─────────────────────────────────────────────────────
organizations = [
    dict(id=1, name="中共阿克塞哈萨克族自治县委", type="党委", level="县处级",
         parent="中共酒泉市委", location="甘肃省酒泉市阿克塞哈萨克族自治县"),
    dict(id=2, name="阿克塞哈萨克族自治县人民政府", type="政府", level="县处级",
         parent="酒泉市人民政府", location="甘肃省酒泉市阿克塞哈萨克族自治县"),
    dict(id=3, name="阿克塞哈萨克族自治县人大常委会", type="人大", level="县处级",
         parent="酒泉市人大常委会", location="甘肃省酒泉市阿克塞哈萨克族自治县"),
    dict(id=4, name="中国人民政治协商会议阿克塞哈萨克族自治县委员会", type="政协", level="县处级",
         parent="政协酒泉市委员会", location="甘肃省酒泉市阿克塞哈萨克族自治县"),
    dict(id=5, name="中共阿克塞哈萨克族自治县纪律检查委员会", type="党委", level="县处级",
         parent="中共阿克塞哈萨克族自治县委", location="甘肃省酒泉市阿克塞哈萨克族自治县"),
    dict(id=6, name="中共阿克塞哈萨克族自治县委宣传部", type="党委", level="乡科级",
         parent="中共阿克塞哈萨克族自治县委", location="甘肃省酒泉市阿克塞哈萨克族自治县"),
    dict(id=7, name="阿克塞哈萨克族自治县公安局", type="政府", level="乡科级",
         parent="阿克塞哈萨克族自治县人民政府", location="甘肃省酒泉市阿克塞哈萨克族自治县"),
    dict(id=8, name="酒泉市人民政府", type="政府", level="地厅级",
         parent="甘肃省人民政府", location="甘肃省酒泉市"),
    dict(id=9, name="酒泉市生态环境局", type="政府", level="地厅级（市直）",
         parent="酒泉市人民政府", location="甘肃省酒泉市"),
    dict(id=10, name="敦煌市人民政府", type="政府", level="县处级",
         parent="酒泉市人民政府", location="甘肃省酒泉市敦煌市"),
]

# ── Positions ─────────────────────────────────────────────────────────
positions = [
    # 张桐
    dict(person_id=pid("zhang_tong"), org_id=1, title="阿克塞哈萨克族自治县委书记",
         start_date="2026-01", end_date="", rank="县处级正职", note="接替陶涛"),
    dict(person_id=pid("zhang_tong"), org_id=9, title="酒泉市生态环境局党组书记、局长",
         start_date="", end_date="2026-01", rank="县处级正职", note="调任阿克塞县委书记前任职"),
    # 库美斯剑
    dict(person_id=pid("kumeisijian"), org_id=2, title="阿克塞哈萨克族自治县长",
         start_date="2021", end_date="", rank="县处级正职", note="接替哈里别克"),
    dict(person_id=pid("kumeisijian"), org_id=1, title="阿克塞哈萨克族自治县委副书记",
         start_date="2021", end_date="", rank="县处级副职", note=""),
    # 陶涛
    dict(person_id=pid("tao_tao"), org_id=8, title="酒泉市人民政府副市长",
         start_date="2026-01", end_date="", rank="地厅级副职", note="2026年1月15日酒泉市五届人大六次会议选举"),
    dict(person_id=pid("tao_tao"), org_id=1, title="阿克塞哈萨克族自治县委书记",
         start_date="2021-04", end_date="2025-12", rank="县处级正职", note="接替前任；后升任酒泉市副市长"),
    # 张鹏
    dict(person_id=pid("zhang_peng"), org_id=1, title="阿克塞哈萨克族自治县委副书记",
         start_date="2025", end_date="", rank="县处级副职", note=""),
    dict(person_id=pid("zhang_peng"), org_id=2, title="阿克塞哈萨克族自治县委常委、常务副县长（人选）",
         start_date="2024-04", end_date="2025", rank="县处级副职", note="调任阿克塞"),
    # 韩虎
    dict(person_id=pid("han_hu"), org_id=5, title="阿克塞哈萨克族自治县委常委、纪委书记、监委主任",
         start_date="", end_date="", rank="县处级副职", note="任职时间待确认"),
    # 冯辉昌
    dict(person_id=pid("feng_huichang"), org_id=3, title="阿克塞哈萨克族自治县人大常委会主任",
         start_date="", end_date="", rank="县处级正职", note=""),
    # 雪莲
    dict(person_id=pid("xuelian"), org_id=4, title="阿克塞哈萨克族自治县政协主席",
         start_date="", end_date="", rank="县处级正职", note=""),
    # 杨国平
    dict(person_id=pid("yang_guoping"), org_id=2, title="阿克塞哈萨克族自治县人民政府副县长",
         start_date="", end_date="", rank="县处级副职", note=""),
    # 巴依哈孜
    dict(person_id=pid("bayihazi"), org_id=2, title="阿克塞哈萨克族自治县人民政府副县长",
         start_date="", end_date="", rank="县处级副职", note="分管农牧、乡村振兴"),
    # 卢保健
    dict(person_id=pid("lu_baojian"), org_id=2, title="阿克塞哈萨克族自治县人民政府副县长",
         start_date="2025-05-27", end_date="", rank="县处级副职", note=""),
    # 哈里别克
    dict(person_id=pid("halibieke"), org_id=8, title="酒泉市人民政府副市长",
         start_date="", end_date="", rank="地厅级副职", note="升任时间待确认"),
    dict(person_id=pid("halibieke"), org_id=2, title="阿克塞哈萨克族自治县长",
         start_date="2016", end_date="2021", rank="县处级正职", note="接替银雁"),
    # 银雁
    dict(person_id=pid("yin_yan"), org_id=2, title="阿克塞哈萨克族自治县长",
         start_date="2011-10", end_date="2016-08", rank="县处级正职",
         note="2011年10月正式当选；2025年8月被查"),
    # 张健
    dict(person_id=pid("zhang_jian"), org_id=6, title="阿克塞哈萨克族自治县委常委、宣传部部长",
         start_date="2024", end_date="", rank="县处级副职", note="此前任肃州区委办公室主任"),
    # 武海龙
    dict(person_id=pid("wu_hailong"), org_id=7, title="阿克塞哈萨克族自治县人民政府副县长、县公安局局长",
         start_date="2024", end_date="", rank="县处级副职", note="此前任金塔县公安局党委副书记、政委"),
    # 孟军政
    dict(person_id=pid("meng_junzheng"), org_id=10, title="敦煌市人民政府副市长、市公安局局长",
         start_date="2024", end_date="", rank="县处级副职", note="调离阿克塞"),
    dict(person_id=pid("meng_junzheng"), org_id=7, title="阿克塞哈萨克族自治县人民政府副县长、县公安局局长",
         start_date="", end_date="2024", rank="县处级副职", note="调任敦煌"),
    # 白振林
    dict(person_id=pid("bai_zhenlin"), org_id=1, title="阿克塞哈萨克族自治县委副书记",
         start_date="", end_date="2024-04", rank="县处级副职", note="调离"),
    # 毛学文
    dict(person_id=pid("mao_xuewen"), org_id=2, title="阿克塞哈萨克族自治县委常委、常务副县长",
         start_date="", end_date="2024-04", rank="县处级副职", note="拟任党委副书记"),
]

# ── Relationships ─────────────────────────────────────────────────────
relationships = [
    dict(person_a=pid("zhang_tong"), person_b=pid("kumeisijian"),
         type="上下级", context="张桐任县委书记后与县长库美斯剑搭班",
         overlap_org="阿克塞县委/县政府", overlap_period="2026-至今"),
    dict(person_a=pid("tao_tao"), person_b=pid("kumeisijian"),
         type="上下级", context="陶涛任县委书记期间与县长库美斯剑搭班",
         overlap_org="阿克塞县委/县政府", overlap_period="2021-2025"),
    dict(person_a=pid("tao_tao"), person_b=pid("halibieke"),
         type="同僚", context="陶涛任县委书记初期与县长哈里别克共事",
         overlap_org="阿克塞县委/县政府", overlap_period="2021"),
    dict(person_a=pid("zhang_peng"), person_b=pid("zhang_tong"),
         type="上下级", context="张鹏任副书记配合书记张桐工作",
         overlap_org="阿克塞县委", overlap_period="2026-至今"),
    dict(person_a=pid("han_hu"), person_b=pid("zhang_tong"),
         type="上下级", context="纪委书记韩虎在县委班子中配合书记张桐",
         overlap_org="阿克塞县委", overlap_period="2026-至今"),
    dict(person_a=pid("han_hu"), person_b=pid("tao_tao"),
         type="上下级", context="纪委书记韩虎在陶涛任书记期间任职",
         overlap_org="阿克塞县委", overlap_period="2023-2025"),
    dict(person_a=pid("zhang_tong"), person_b=pid("feng_huichang"),
         type="同僚", context="县委-人大领导关系",
         overlap_org="阿克塞县", overlap_period="2026-至今"),
    dict(person_a=pid("zhang_tong"), person_b=pid("xuelian"),
         type="同僚", context="县委-政协领导关系",
         overlap_org="阿克塞县", overlap_period="2026-至今"),
    dict(person_a=pid("kumeisijian"), person_b=pid("yang_guoping"),
         type="上下级", context="县长与副县长",
         overlap_org="阿克塞县人民政府", overlap_period=""),
    dict(person_a=pid("kumeisijian"), person_b=pid("bayihazi"),
         type="上下级", context="县长与副县长",
         overlap_org="阿克塞县人民政府", overlap_period=""),
    dict(person_a=pid("kumeisijian"), person_b=pid("lu_baojian"),
         type="上下级", context="县长与副县长",
         overlap_org="阿克塞县人民政府", overlap_period="2025-至今"),
    dict(person_a=pid("yin_yan"), person_b=pid("halibieke"),
         type="前后任", context="银雁任县长后由哈里别克接任",
         overlap_org="阿克塞县人民政府", overlap_period="2016"),
    dict(person_a=pid("zhang_jian"), person_b=pid("zhang_tong"),
         type="上下级", context="张健（宣传部部长）在张桐任书记后留任县委班子",
         overlap_org="阿克塞县委", overlap_period="2026-至今"),
    dict(person_a=pid("wu_hailong"), person_b=pid("kumeisijian"),
         type="上下级", context="武海龙（公安局长）在县长领导下工作",
         overlap_org="阿克塞县政府", overlap_period="2024-至今"),
    dict(person_a=pid("tao_tao"), person_b=pid("zhang_tong"),
         type="前后任", context="陶涛离任阿克塞县委书记后由张桐接任",
         overlap_org="阿克塞县委", overlap_period="2026"),
    dict(person_a=pid("bai_zhenlin"), person_b=pid("zhang_peng"),
         type="前后任", context="白振林离任县委副书记后由张鹏接任",
         overlap_org="阿克塞县委", overlap_period="2024-2025"),
    dict(person_a=pid("mao_xuewen"), person_b=pid("zhang_peng"),
         type="前后任", context="毛学文离任常务副县长后由张鹏接任常务副县长人选",
         overlap_org="阿克塞县人民政府", overlap_period="2024"),
    dict(person_a=pid("meng_junzheng"), person_b=pid("wu_hailong"),
         type="前后任", context="孟军政调任敦煌后由武海龙接任阿克塞公安局长",
         overlap_org="阿克塞县公安局", overlap_period="2024"),
]

if __name__ == "__main__":
    run_build(
        slug="阿克塞哈萨克族自治县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "阿克塞哈萨克族自治县_network.db",
        gexf_path=GRAPH_DIR / "阿克塞哈萨克族自治县_network.gexf",
        overwrite=True,
    )
