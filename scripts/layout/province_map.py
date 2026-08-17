"""Province name helpers for the filesystem layout migration.

Maps Chinese province/autonomous-region/municipality names to the slug style
used elsewhere in the repo (e.g. ``data/provinces/<slug>/``).
"""

from __future__ import annotations

# Chinese province/full region name -> slug (matches data/provinces/<slug>)
PROVINCE_TO_SLUG: dict[str, str] = {
    "安徽省": "anhui",
    "北京市": "beijing",
    "重庆": "chongqing",
    "重庆市": "chongqing",
    "福建省": "fujian",
    "甘肃省": "gansu",
    "广东省": "guangdong",
    "广西": "guangxi",
    "广西壮族自治区": "guangxi",
    "贵州省": "guizhou",
    "海南省": "hainan",
    "河北省": "hebei",
    "黑龙江省": "heilongjiang",
    "河南省": "henan",
    "湖北省": "hubei",
    "湖南省": "hunan",
    "内蒙古自治区": "inner_mongolia",
    "内蒙古": "inner_mongolia",
    "江苏省": "jiangsu",
    "江西省": "jiangxi",
    "吉林省": "jilin",
    "辽宁省": "liaoning",
    "宁夏回族自治区": "ningxia",
    "宁夏": "ningxia",
    "青海省": "qinghai",
    "陕西省": "shaanxi",
    "山东省": "shandong",
    "上海市": "shanghai",
    "山西省": "shanxi",
    "四川省": "sichuan",
    "天津市": "tianjin",
    "新疆维吾尔自治区": "xinjiang",
    "新疆": "xinjiang",
    "西藏自治区": "xizang",
    "西藏": "xizang",
    "云南省": "yunnan",
    "浙江省": "zhejiang",
}

# slug -> human full name (for display / reverse lookups)
SLUG_TO_PROVINCE: dict[str, str] = {v: k for k, v in PROVINCE_TO_SLUG.items()}

# Known ambiguous "省+市" merged cells found in legacy filenames, mapped to slug.
# Every entry is reviewed; anything not listed goes to the override/anomaly bucket.
LEGACY_REGION_TO_SLUG: dict[str, str] = {
    "河北省张家口市赤城县": "hebei",
}

# Reviewed manual overrides for person files whose first field after the date
# is a city/county name rather than a province (orphan cases from legacy builds).
# Each is hand-checked: <first-field> -> province slug.
PERSON_REGION_OVERRIDE: dict[str, str] = {
    "beijing": "beijing",
    "永泰": "fujian",       # 永泰县，福州市
    "泸州": "sichuan",       # 泸州市；纳溪区
    "阳曲县": "shanxi",      # 阳曲县，太原市
    "洛阳市": "henan",
    "北京市": "beijing",
}


def province_slug(name: str) -> str | None:
    """Return the province slug for a province full name, or None if unknown."""
    return PROVINCE_TO_SLUG.get(name)


def resolve_any_province_slug(token: str) -> str | None:
    """Resolve a free-form province-ish token (isolated or merged with a city)."""
    if token in PROVINCE_TO_SLUG:
        return PROVINCE_TO_SLUG[token]
    # merged "省+市" cells
    for legacy, slug in LEGACY_REGION_TO_SLUG.items():
        if token == legacy:
            return slug
    for pname, slug in PROVINCE_TO_SLUG.items():
        if token.startswith(pname):
            return slug
    return None