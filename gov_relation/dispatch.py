"""Generate queue-driven investigation dispatch prompts."""

from __future__ import annotations

from dataclasses import dataclass

from .log import get_logger
from .slugs import artifact_paths
from .todo import TodoItem, item_summary

logger = get_logger(__name__)


@dataclass(frozen=True)
class DispatchPlan:
    task: dict
    model_intent: str
    prompt: str
    suggested_command: str


def build_dispatch_prompt(item: TodoItem, model_intent: str = "standard") -> str:
    task = item_summary(item)
    paths = artifact_paths(task["region"])
    targets = " & ".join(task["target_roles"])
    parent_city = task["parent_city"] or ""
    return f"""Use the china-gov-network skill at .agents/skills/china-gov-network.

Non-negotiable execution rules:
- You are the end-to-end executor, not a planner. Do not stop after creating a plan or launching subagents.
- If you use subagents, wait for their results, synthesize them, and continue through artifact creation yourself.
- If subagents are unavailable, asynchronous, or return incomplete information, continue the investigation directly with the available tools.
- Do not call scripts/todo_queue.py claim/done/fail/release. The external worker owns queue state.
- Do not finish with only notes, todos, or a staging directory. A successful run must leave the canonical build script, SQLite DB, GEXF graph, and person JSON files after validation and promotion.
- If evidence is incomplete, encode gaps with confidence/open_questions, but still create structurally valid artifacts from confirmed/plausible evidence.
- Do not repeatedly call failing search providers. If Exa is rate-limited, stop using Exa for this task. If Baidu returns 403/captcha, treat Baidu as unavailable. If a government host times out twice, try alternate official URL patterns, parent-city/organization-department sites, Jina Reader (`https://r.jina.ai/http://r.jina.ai/http://...`), local repo artifacts, and partial-evidence artifact mode.
- Under degraded web access, still produce artifacts with explicit uncertainty. Put missing biography fields in person JSON `open_questions` and `report/open_gaps.md` rather than failing with no build/db/gexf.

Task:
- task_id: {task["task_id"]}
- province: {task["province"]}
- parent_city: {parent_city}
- region: {task["region"]}
- level: {task["level"]}
- targets: {targets}
- model_intent: {model_intent}

Expected artifact paths:
- staging_dir: data/tmp/{task["task_id"]}/
- build_script: data/tmp/{task["task_id"]}/{paths["build_script"]}
- database: data/tmp/{task["task_id"]}/{paths["db_output"].split("/")[-1]}
- gexf: data/tmp/{task["task_id"]}/{paths["gexf_output"].split("/")[-1]}
- person_json_pattern: data/tmp/{task["task_id"]}/YYYYMMDD-{task["province"]}-{parent_city or task["region"]}-{{job}}-{{name}}.json

Canonical destination after validation:
- build_script: {paths["build_script"]}
- database: {paths["db_output"]}
- gexf: {paths["gexf_output"]}
- person_json_dir: data/persons/

Required workflow:
1. Run Phase 0 repository preflight.
2. Read relevant references from .agents/skills/china-gov-network/references:
   - investigation_stages.md
   - subagent_dispatch.md
   - source_fallbacks.md
   - person_graph_json.md
   - gexf_pattern.md when writing graph output
3. Research current officeholders, leadership roster, biographies, predecessor/successor moves, relationship evidence, governance/professional profile, and open gaps.
4. Write all newly generated artifacts into the staging directory first. Do not write new build scripts into repo root directly.
5. Validate with py_compile, script execution, json.tool for person JSON, and scripts/process_tmp.py data/tmp/{task["task_id"]}.
6. Promote with scripts/process_tmp.py data/tmp/{task["task_id"]} --apply only after the dry run is clean.
7. Run scripts/inventory.py after promotion.
8. Before exiting, verify these canonical paths exist:
   - {paths["build_script"]}
   - {paths["db_output"]}
   - {paths["gexf_output"]}
   - at least two data/persons/YYYYMMDD-...json files for the core leaders when names are known
"""


def build_dispatch_plan(item: TodoItem, model_intent: str = "standard") -> DispatchPlan:
    task = item_summary(item)
    prompt = build_dispatch_prompt(item, model_intent=model_intent)
    suggested_command = "opencode run --model iagent/standard '<PROMPT_FROM_STDOUT>'"
    return DispatchPlan(task=task, model_intent=model_intent, prompt=prompt, suggested_command=suggested_command)
