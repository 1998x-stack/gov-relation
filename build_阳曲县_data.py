#!/usr/bin/env python3
"""Build 阳曲县 leadership network (updated 2026-07-26 with latest changes)."""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "阳曲县"

PERSONS = [
    # 1-10: 县委常委
    {"id":1,"name":"姬发军","gender":"男","ethnicity":"汉族","birth":"1975.04","birthplace":"山西娄烦","education":"中央党校大学/工学硕士","party_join":"2000.08","work_start":"1996.08","current_post":"县委书记","current_org":"中共阳曲县委员会","source":"https://www.shanxishangren.com/b2b/news/show.php?itemid=170127"},
    {"id":2,"name":"吴英志","gender":"男","ethnicity":"汉族","birth":"1977.04","birthplace":"北京","education":"中央党校研究生","party_join":"","work_start":"1997.07","current_post":"县委副书记、县长","current_org":"阳曲县人民政府","source":"http://epaper.tyrbw.com/tyrb/h5/html5/2025-12/12/content_2_226342.htm"},
    {"id":3,"name":"武晓俊","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委、政法委书记","current_org":"中共阳曲县委政法委员会","source":"https://www.fensifuwu.com/emotion/me/1976445.html"},
    {"id":4,"name":"王庆丰","gender":"男","ethnicity":"汉族","birth":"1970.09","birthplace":"山西阳曲","education":"","party_join":"","work_start":"","current_post":"县委常委、宣传部部长","current_org":"中共阳曲县委宣传部","source":"https://www.shanxishangren.com/b2b/news/show.php?itemid=149650"},
    {"id":5,"name":"郭志红","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委、副县长","current_org":"阳曲县人民政府","source":"https://www.shanxishangren.com/b2b/news/show.php?itemid=149650"},
    {"id":6,"name":"阴笑弘","gender":"女","ethnicity":"汉族","birth":"","birthplace":"山西晋城","education":"","party_join":"","work_start":"","current_post":"县委常委、副县长","current_org":"阳曲县人民政府","source":"https://www.shanxishangren.com/b2b/news/show.php?itemid=160912"},
    {"id":7,"name":"王铮","gender":"男","ethnicity":"汉族","birth":"1972.05","birthplace":"","education":"大学","party_join":"","work_start":"","current_post":"县委常委、县纪委书记、监委主任","current_org":"中共阳曲县纪律检查委员会","source":"https://www.toutiao.com/article/7647667755906335295/"},
    {"id":8,"name":"马文杰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委、组织部部长","current_org":"中共阳曲县委组织部","source":"http://cmsc.apcreports.org.cn/cmsc/news/32298.html"},
    {"id":9,"name":"范旭宇","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委、人武部政委","current_org":"阳曲县人民武装部","source":"https://www.thepaper.cn/newsDetail_forward_28316676"},
    {"id":10,"name":"邹亮","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委、人武部部长","current_org":"阳曲县人民武装部","source":""},
    # 11-17: 县政府副县长及人大政协
    {"id":11,"name":"马有利","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"阳曲县人民政府","source":"https://www.shanxishangren.com/b2b/news/show.php?itemid=149650"},
    {"id":12,"name":"张建","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"阳曲县人民政府","source":"https://www.shanxishangren.com/b2b/news/show.php?itemid=149650"},
    {"id":13,"name":"游胜文","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"阳曲县人民政府","source":"https://www.shanxishangren.com/b2b/news/show.php?itemid=149650"},
    {"id":14,"name":"李峰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长、县公安局局长","current_org":"阳曲县公安局","source":"https://www.163.com/dy/article/KU37ISV705149E7M.html"},
    {"id":15,"name":"乔馨","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"阳曲县人民政府","source":"https://www.163.com/dy/article/KU37ISV705149E7M.html"},
    {"id":16,"name":"王志勇","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县人大常委会主任","current_org":"阳曲县人大常委会","source":"http://www.sx.chinanews.com.cn/news/2025/0429/240615.html"},
    {"id":17,"name":"于文成","gender":"男","ethnicity":"汉族","birth":"1970.06","birthplace":"山西阳曲","education":"中央党校大学","party_join":"1996.11","work_start":"1991.07","current_post":"县政协主席","current_org":"政协阳曲县委员会","source":"https://www.newton.com.tw/wiki/於文成/58597057"},
    # 18-20: 前任县委书记
    {"id":18,"name":"李京京","gender":"男","ethnicity":"汉族","birth":"1977.01","birthplace":"山东沂水","education":"研究生/工程硕士","party_join":"1996.10","work_start":"1997.07","current_post":"清徐县委书记","current_org":"中共清徐县委员会","source":"https://baike.baidu.com/item/李京京/19926837"},
    {"id":19,"name":"裴耀军","gender":"男","ethnicity":"汉族","birth":"1969.07","birthplace":"山西榆社","education":"大学","party_join":"1996.06","work_start":"1991.06","current_post":"省工商联党组书记（原阳曲县委书记）","current_org":"山西省工商联","source":"https://baike.baidu.com/item/裴耀军/7381004"},
    {"id":20,"name":"刘晋萍","gender":"女","ethnicity":"汉族","birth":"1965.01","birthplace":"山西五台","education":"中央党校研究生","party_join":"","work_start":"","current_post":"吕梁市委常委、副市长（原阳曲县委书记）","current_org":"中共吕梁市委","source":"https://www.thepaper.cn/newsDetail_forward_1417799"},
    # 21-23: 2026.05免职
    {"id":21,"name":"孙慧生","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"原县委常委、副县长（2026.05免职）","current_org":"","source":"https://www.163.com/dy/article/KU37ISV705149E7M.html"},
    {"id":22,"name":"申彩萍","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"原副县长（2026.05免职）","current_org":"","source":"https://www.163.com/dy/article/KU37ISV705149E7M.html"},
    {"id":23,"name":"刘波","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"原副县长、县公安局局长（2026.05免职）","current_org":"","source":"https://www.163.com/dy/article/KU37ISV705149E7M.html"},
]

O = [
    {"id":1,"name":"中共阳曲县委员会","type":"党委","level":"县处级","parent":"中共太原市委","location":"阳曲县"},
    {"id":2,"name":"阳曲县人民政府","type":"政府","level":"县处级","parent":"太原市人民政府","location":"阳曲县"},
    {"id":3,"name":"中共阳曲县纪律检查委员会","type":"纪委","level":"县处级","parent":"中共太原市纪委","location":"阳曲县"},
    {"id":4,"name":"阳曲县人大常委会","type":"人大","level":"县处级","parent":"太原市人大常委会","location":"阳曲县"},
    {"id":5,"name":"政协阳曲县委员会","type":"政协","level":"县处级","parent":"政协太原市委员会","location":"阳曲县"},
    {"id":6,"name":"中共阳曲县委政法委员会","type":"党委部门","level":"","parent":"中共阳曲县委员会","location":"阳曲县"},
    {"id":7,"name":"中共阳曲县委宣传部","type":"党委部门","level":"","parent":"中共阳曲县委员会","location":"阳曲县"},
    {"id":8,"name":"中共阳曲县委组织部","type":"党委部门","level":"","parent":"中共阳曲县委员会","location":"阳曲县"},
    {"id":9,"name":"阳曲县人民武装部","type":"军事","level":"","parent":"太原警备区","location":"阳曲县"},
    {"id":10,"name":"阳曲县公安局","type":"政府组成部门","level":"乡科级","parent":"阳曲县人民政府","location":"阳曲县"},
    {"id":11,"name":"中共清徐县委员会","type":"党委","level":"县处级","parent":"中共太原市委","location":"清徐县"},
    {"id":12,"name":"阳曲现代农业产业示范区","type":"开发区","level":"省级","parent":"阳曲县人民政府","location":"阳曲县"},
]

POS = [
    {"person_id":1,"org_id":1,"title":"县委书记","start_date":"2025.04","end_date":"","rank":"正处级","note":"接替李京京"},
    {"person_id":1,"org_id":2,"title":"县长（兼）","start_date":"2022.05","end_date":"2025.12","rank":"正处级","note":""},
    {"person_id":1,"org_id":2,"title":"代县长","start_date":"2022.04","end_date":"2022.05","rank":"正处级","note":""},
    {"person_id":1,"org_id":12,"title":"示范区党工委书记、管委会主任","start_date":"2025.04","end_date":"","rank":"","note":"兼"},
    {"person_id":2,"org_id":2,"title":"县长","start_date":"2025.12","end_date":"","rank":"正处级","note":""},
    {"person_id":2,"org_id":1,"title":"县委副书记","start_date":"","end_date":"","rank":"副处级","note":""},
    {"person_id":3,"org_id":6,"title":"政法委书记","start_date":"","end_date":"","rank":"副处级","note":"兼县委常委"},
    {"person_id":4,"org_id":7,"title":"宣传部部长","start_date":"","end_date":"","rank":"副处级","note":"兼县委常委"},
    {"person_id":5,"org_id":2,"title":"副县长","start_date":"","end_date":"","rank":"副处级","note":"兼县委常委"},
    {"person_id":6,"org_id":2,"title":"副县长","start_date":"","end_date":"","rank":"副处级","note":"兼县委常委"},
    {"person_id":7,"org_id":3,"title":"纪委书记、监委主任","start_date":"","end_date":"","rank":"副处级","note":"兼县委常委"},
    {"person_id":8,"org_id":8,"title":"组织部部长","start_date":"","end_date":"","rank":"副处级","note":"兼县委常委"},
    {"person_id":9,"org_id":9,"title":"政委","start_date":"","end_date":"","rank":"副处级","note":"兼县委常委"},
    {"person_id":10,"org_id":9,"title":"部长","start_date":"","end_date":"","rank":"副处级","note":"兼县委常委"},
    {"person_id":11,"org_id":2,"title":"副县长","start_date":"","end_date":"","rank":"副处级","note":"住建交通"},
    {"person_id":12,"org_id":2,"title":"副县长","start_date":"","end_date":"","rank":"副处级","note":"教育文旅审批"},
    {"person_id":13,"org_id":2,"title":"副县长","start_date":"","end_date":"","rank":"副处级","note":"工信统计园区"},
    {"person_id":14,"org_id":10,"title":"县公安局局长","start_date":"2026.05","end_date":"","rank":"正科级","note":"兼副县长"},
    {"person_id":14,"org_id":2,"title":"副县长","start_date":"2026.05","end_date":"","rank":"副处级","note":""},
    {"person_id":15,"org_id":2,"title":"副县长","start_date":"2026.05","end_date":"","rank":"副处级","note":""},
    {"person_id":16,"org_id":4,"title":"人大常委会主任","start_date":"","end_date":"","rank":"正处级","note":""},
    {"person_id":17,"org_id":5,"title":"政协主席","start_date":"2021.04","end_date":"","rank":"正处级","note":""},
    {"person_id":18,"org_id":11,"title":"县委书记","start_date":"2025.04","end_date":"","rank":"正处级","note":"清徐"},
    {"person_id":18,"org_id":1,"title":"县委书记","start_date":"2022.03","end_date":"2025.04","rank":"正处级","note":"阳曲"},
    {"person_id":18,"org_id":2,"title":"县长","start_date":"2019.02","end_date":"2022.03","rank":"正处级","note":"阳曲"},
    {"person_id":19,"org_id":1,"title":"县委书记","start_date":"约2017","end_date":"2022.03","rank":"正处级","note":"接替刘晋萍"},
    {"person_id":19,"org_id":2,"title":"县长","start_date":"2016.08","end_date":"约2017","rank":"正处级","note":""},
    {"person_id":20,"org_id":1,"title":"县委书记","start_date":"2016.01","end_date":"约2017","rank":"正处级","note":""},
    {"person_id":20,"org_id":2,"title":"县长","start_date":"2013.04","end_date":"2016.01","rank":"正处级","note":""},
    {"person_id":21,"org_id":2,"title":"常务副县长","start_date":"","end_date":"2026.05","rank":"副处级","note":"已免职"},
    {"person_id":22,"org_id":2,"title":"副县长","start_date":"","end_date":"2026.05","rank":"副处级","note":"已免职"},
    {"person_id":23,"org_id":10,"title":"县公安局局长","start_date":"","end_date":"2026.05","rank":"正科级","note":"已免职"},
    {"person_id":23,"org_id":2,"title":"副县长","start_date":"","end_date":"2026.05","rank":"副处级","note":"已免职"},
]

# ── Relationships ──────────────────────────────────────────────────────
RELS = [
    # 书记-县长传承链
    {"person_a": 4, "person_b": 3, "type": "前后任", "context": "刘晋萍→裴耀军：阳曲县委书记前后任（2019年1月交接）", "overlap_org": "中共阳曲县委", "overlap_period": "2016-2019"},
    {"person_a": 3, "person_b": 2, "type": "前后任", "context": "裴耀军→李京京：阳曲县委书记前后任（2022年4月交接）", "overlap_org": "中共阳曲县委", "overlap_period": "2019-2022"},
    {"person_a": 2, "person_b": 1, "type": "前后任", "context": "李京京→姬发军：阳曲县委书记前后任（2025年4月交接）", "overlap_org": "中共阳曲县委", "overlap_period": "2022-2025"},
    # 县长传承链
    {"person_a": 4, "person_b": 3, "type": "前后任", "context": "刘晋萍→裴耀军：阳曲县长前后任（2016年8月交接）", "overlap_org": "阳曲县人民政府", "overlap_period": "2013-2016"},
    {"person_a": 3, "person_b": 2, "type": "前后任", "context": "裴耀军→李京京：阳曲县长前后任（2019年1月交接）", "overlap_org": "阳曲县人民政府", "overlap_period": "2016-2019"},
    {"person_a": 2, "person_b": 1, "type": "前后任", "context": "李京京→姬发军：阳曲县长前后任（2022年4月交接）", "overlap_org": "阳曲县人民政府", "overlap_period": "2019-2022"},
    {"person_a": 1, "person_b": 5, "type": "前后任", "context": "姬发军→吴英志：阳曲县长前后任（2025年12月交接）", "overlap_org": "阳曲县人民政府", "overlap_period": "2022-2025"},
    # 共事关系（县委常委会内）
    {"person_a": 2, "person_b": 1, "type": "共事", "context": "李京京（书记）与姬发军（县长）在阳曲县委共事", "overlap_org": "中共阳曲县委", "overlap_period": "2022-2025"},
    {"person_a": 3, "person_b": 2, "type": "共事", "context": "裴耀军（书记）与李京京（县长）在阳曲县委共事", "overlap_org": "中共阳曲县委", "overlap_period": "2019-2022"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "李京京（书记）与吴英志（副书记）在阳曲县委共事", "overlap_org": "中共阳曲县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "姬发军（书记/县长）与吴英志（副书记→县长）在阳曲县委共事", "overlap_org": "中共阳曲县委", "overlap_period": ""},
    # 跨县调动关系
    {"person_a": 2, "person_b": 16, "type": "前后任", "context": "李京京接替王剑峰任清徐县委书记", "overlap_org": "中共清徐县委", "overlap_period": "2025"},
    {"person_a": 5, "person_b": 3, "type": "跨县调动", "context": "吴英志从清徐县委常委调任阳曲（县委常委→副书记→县长）", "overlap_org": "", "overlap_period": ""},
    # 娄烦籍官员关联
    {"person_a": 1, "person_b": 17, "type": "同乡", "context": "姬发军与孙晋生均为山西娄烦人", "overlap_org": "", "overlap_period": ""},
    # 书记与下级的共事
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "姬发军（书记/县长）与武晓俊（副书记/政法委书记）在阳曲共事", "overlap_org": "中共阳曲县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "姬发军（县长/书记）与孙慧生（常务副县长）在县政府共事", "overlap_org": "阳曲县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "姬发军（县长）与马有利（副县长）在县政府共事", "overlap_org": "阳曲县人民政府", "overlap_period": ""},
]


def main() -> None:
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=O,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DATABASE_DIR / "阳曲县_network.db",
        gexf_path=GRAPH_DIR / "阳曲县_network.gexf",
        overwrite=True,
    )


if __name__ == "__main__":
    main()
