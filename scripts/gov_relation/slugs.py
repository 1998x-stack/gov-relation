"""Filename slug helpers for region build artifacts."""

from __future__ import annotations

REGION_SLUGS: dict[str, str] = {
    "安义县": "anyi",
    "东湖区": "donghu",
    "红谷滩区": "honggutan",
    "景德镇市": "jingdezhen",
    "进贤县": "jinxian",
    "南昌市": "nanchang_city",
    "南昌县": "nanchang_county",
    "萍乡市": "pingxiang",
    "青山湖区": "qingshanhu",
    "青云谱区": "qingyunpu",
    "新余市": "xinyu",
    "鹰潭市": "yingtan",
    "月湖区": "yuehu",
    "濂溪区": "lianxi",
    "柴桑区": "chaisang",
}


def region_slug(region: str) -> str:
    """Return the preferred artifact slug for a Chinese region name."""
    return REGION_SLUGS.get(region, region)


def artifact_paths(region: str) -> dict[str, str]:
    """Return conventional build artifact paths for a region."""
    slug = region_slug(region)
    return {
        "slug": slug,
        "build_script": f"build_{slug}_data.py",
        "db_output": f"data/database/{slug}_network.db",
        "gexf_output": f"data/graph/{slug}_network.gexf",
    }

