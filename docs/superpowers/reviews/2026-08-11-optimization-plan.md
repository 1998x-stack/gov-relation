# v3 前序 Phase 优化清单(SubAgentReview 后)

- **日期:** 2026-08-11
- **来源:** 三份审查报告 `docs/superpowers/reviews/2026-08-11-review-*.md`(Phase 1 CHANGES-REQUESTED / Phase 2 CHANGES-REQUESTED / Phase 3 APPROVED)
- **原则:** 先文档同步 → 再小步代码修复 → 提交与决策项逐项确认 → 最后进 Phase 4

---

## A. 文档/规范同步(已执行,commit `e4614908c`)

- [x] **spec §11 Phase 2 废弃标注** — `schema.py` 升 v3 DDL、`ADDITIVE_SCHEMA_UPGRADES` 纳入 2.1.0 两处旧方案已划除并指向 Phase 2 计划 Task 1 废弃声明。
- [x] **spec §4.5 `gold_current_positions` 语义同步** — 注明已实现视图读 `positions.is_current=1`。
- [x] **spec §9.2 `BuildScriptFactory.generate()` 签名同步**。
- [x] **spec 顶部修订注记**。
- [x] **Phase 1 清单过期数字修正**(25→32 测试、222→241 passed)。

## B. 功能/健壮性修复(已实现并验证)

- [x] **Phase 1 F4 修复** — `build_factory` 生成脚本改由 `_repo_root()` 沿父目录链向上搜索 `gov_relation/` 定位仓库根,不再硬编码 `parents[2]`(`276320464`;测试同步更新:tmp 内建 `gov_relation/` 标记验证)。
- [x] **Phase 3 人名兜底解析守卫** — 对齐计划参考实现(`isdigit()` + 长度守卫;8 位日期前缀丢 1 段、4 位年份丢 3 段、其余保留全部);改后 dry-run 复跑:unmatched=0/ambiguous=0/holdout=4 不变(`bf4c9ee54`)。
- [x] **`gold_current_positions` 语义测试** — 新增 `tests/test_factory/test_gold_views.py` 2 例(仅现任入视图、组织 LEFT JOIN)。

## C. 仓库健康(已按授权执行)

- [x] **补提交** — `276320464`(Phase 1:factory/identity/paths/runner/gexf + 31 省骨架 .gitkeep + 外部数据合并 json + 广西两个新 builder); `20ca249e9`(Phase 2:upgrade 脚本 + platform/schema.py 门禁 + govdb 校验 + 12 例门禁测试); `bf4c9ee54`(Phase 3:迁移回归测试×2 + 人名守卫 + docs/assets 再生成)。docs/reports 日常流水线产物未掺入。
- [x] **data/provinces/ 处置** — 加入 `.gitignore`(`data/provinces/**` + 例外保留目录与 `.gitkeep`),124 个骨架文件入库,11,214 个运行时产物不入库。
- [x] **分歧分支处置** — `worktree-v3-refactor` 分支 + 关联 worktree 已删除(旧实现已被工作树新版取代)。
- [x] **Phase 2 备份缺件注明** — plan Step 3 完成记录已注明 `.pre-v3.bak` 未落盘、历史快照无法补回,要求后续 DB 迁移必须先备份。

## 遗留(非 v3 审查产物,未动)

- docs/reports 海量 untracked HTML = 日常研究流水线产物。
- `process_tmp.py` / `tests/test_process_tmp_province.py` 等 = Phase 4 前置工作,留待 Phase 4 提交。
- `platform/rights.py`、`central.py`、`dispatch.py`、`queue.py` 等 M = 其他并行lane 改动,未入库。

---

**完成标准已达成:** A 全部 + B 全部实现(全量 243 passed、dry-run 门禁不变)+ C 逐项落地 → 可以进入 Phase 4。