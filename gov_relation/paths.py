"""Repository path helpers."""

import re
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
TMP_DIR = DATA_DIR / "tmp"
DISPATCH_STATE_PATH = DATA_DIR / "dispatch_state.json"
DISPATCH_LOCK_DIR = DATA_DIR / "dispatch_state.lock"
DATABASE_DIR = DATA_DIR / "database"
GRAPH_DIR = DATA_DIR / "graph"
JSON_DIR = DATA_DIR / "json"
PERSONS_DIR = DATA_DIR / "persons"
PLATFORM_DIR = DATA_DIR / "platform"
CANONICAL_DB = PLATFORM_DIR / "gov_relation.db"
REPORT_DIR = REPO_ROOT / "report"
DOCS_DIR = REPO_ROOT / "docs"
TODO_PATH = DATA_DIR / "TODO.json"

CENTRAL_DIR = DATA_DIR / "central"
REGISTRY_DB = CENTRAL_DIR / "registry.db"
PROVINCE_DIR = CENTRAL_DIR / "provincial"

PROVINCES_DIR = DATA_DIR / "provinces"

PROVINCE_SLUGS: dict[str, str] = {
    "安徽省": "anhui", "北京市": "beijing", "重庆市": "chongqing",
    "福建省": "fujian", "甘肃省": "gansu", "广东省": "guangdong",
    "广西壮族自治区": "guangxi", "贵州省": "guizhou", "海南省": "hainan",
    "河北省": "hebei", "河南省": "henan", "黑龙江省": "heilongjiang",
    "湖北省": "hubei", "湖南省": "hunan", "吉林省": "jilin",
    "江苏省": "jiangsu", "江西省": "jiangxi", "辽宁省": "liaoning",
    "内蒙古自治区": "inner_mongolia", "宁夏回族自治区": "ningxia",
    "青海省": "qinghai", "山东省": "shandong", "山西省": "shanxi",
    "陕西省": "shaanxi", "上海市": "shanghai", "四川省": "sichuan",
    "天津市": "tianjin", "西藏自治区": "xizang",
    "新疆维吾尔自治区": "xinjiang", "云南省": "yunnan",
    "浙江省": "zhejiang",
}

_UNSAFE_COMPONENT = re.compile(r"[\\/\x00-\x1f\x7f]+")


def repo_path(*parts: str) -> Path:
    """Return a path rooted at the repository."""
    return REPO_ROOT.joinpath(*parts)


def data_path(*parts: str) -> Path:
    """Return a path rooted at data/."""
    return DATA_DIR.joinpath(*parts)


def province_dir(province: str) -> Path:
    """Return the data directory for a Chinese province name or slug."""
    return PROVINCES_DIR / PROVINCE_SLUGS.get(province, province)


def canonical_province_name(province: str) -> str:
    """Return the Chinese province name for either a name or configured slug."""
    if province in PROVINCE_SLUGS:
        return province
    return next(
        (name for name, slug in PROVINCE_SLUGS.items() if slug == province),
        province,
    )


def safe_path_component(value: object) -> str:
    """Return one non-empty filename component without path separators."""
    component = unicodedata.normalize("NFKC", str(value or "")).strip()
    component = _UNSAFE_COMPONENT.sub("_", component).strip(" .")
    return component or "unknown"


def province_build_dir(province: str) -> Path:
    """Return the shared builder directory; filenames must be province-qualified."""
    return REPO_ROOT / "scripts" / "build"


def province_database_dir(province: str) -> Path:
    return province_dir(province) / "database"


def province_graph_dir(province: str) -> Path:
    return province_dir(province) / "graph"


def province_persons_dir(province: str) -> Path:
    return province_dir(province) / "persons"


def province_reports_dir(province: str) -> Path:
    return province_dir(province) / "reports"
