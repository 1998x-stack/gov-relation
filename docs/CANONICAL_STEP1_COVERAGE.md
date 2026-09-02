# 方案 A · 第一步「非破坏汇入」结果报告

日期：2026-09-02　模型：Canonical JSONL + SQLite 备份（SQLite 仅备份）

## 结果：全量汇入 + 一致性验证通过 ✅

| 资产 | legacy 源 | canonical records | 覆盖率 |
| --- | --- | --- | --- |
| 人物档案 | 13,697 文件 | `profile_documents` 13,765 条 | ~100% |
| legacy 地区库 | 652 个 `*.db` | `datasets` 7,386 条 | 全部收录 |
| 省分库 | 98 个 | 同上（并入 datasets/raw_records） | 全部收录 |
| 统一平台库 | 190MB | 20 条 JSONL 流 | `verify` 逐字节一致 |

**SQLite 备份**：`data/database/platform.db` 由 `data/records/` 重建，`gov2 verify` → `consistent=True`（20 流 count+sha256 全等）。

## 20 条 canonical 流的规模（verify 基准）

| 流 | 行数 |
| --- | ---: |
| profile_documents | 13,765 |
| persons | 27,463 |
| organizations | 18,091 |
| positions | 26,318 |
| relationships | 20,596 |
| sources | 12,927 |
| claims | 26,715 |
| raw_records | 39,493 |
| entity_provenance | 39,242 |
| evidence_links | 38,778 |
| datasets | 7,386 |
| jurisdictions | 2,846 |
| resolution_candidates | 15,114 |
| person_statuses | 14,988 |
| person_aliases / quality_issues | 36 / 719 |
| ingest_runs | 1 |
| （rights_* 为空，待签名接入） | — |

## 本步骤修复的性能/健壮性缺陷（由 101 分钟故障暴露）

1. **O(N²) → O(N) 幂等追加**：`_append_idempotent` 原先每条记录重读整份 JSONL；改为一次性载入 id 集合。实测导入从 ~100 分钟降到 **2 秒**（约 3000×）。
2. **SQLite 备份原子重建**：改为写临时文件 → 成功后 `os.replace` 原子替换，失败自动清理、不残留半成品/WAL。
3. **`NOT NULL` 语义修正**：SQLite 是 JSONL 的镜像，行可能缺值。备份建表时去除 `NOT NULL`（保留 PK/类型/索引），使「JSONL 有 NULL → SQLite 存 NULL」合法化，避免 recycle 因 `raw_record_id NOT NULL` 崩溃。person_id/raw_record_id 等外键型引用列允许空。

## 下一步（破坏性替换，需你拍板）
- 步骤 2：删除 legacy SQLite 事实源 `data/platform/gov_relation.db`、旧 `data/database/*.db`、`data/graph`、`data/persons`、`report` 由 records/备份替代；`scripts`/`serve`/前端改造读 canonical。
- 步骤 3：2342 个 `build_*_data.py` 改为写 canonical JSONL（而非 legacy DB）。
- git 策略：`data/records`（198M）+ 是否版本化、是否按省分区。