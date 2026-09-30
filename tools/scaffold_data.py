"""results/ と reviews/ のスタブ JSON を生成する。
既存ファイルは上書きしない（計測済みデータを壊さないため）。

usage: python tools/scaffold_data.py
"""
import json
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
TASKS = ["T1", "T2", "T3", "T4", "T5", "T6"]

MATRIX_KEYS = [
    "form", "os_windows", "os_mac", "os_linux",
    "byok", "custom_endpoint", "local_llm", "proxy_key_hiding",
    "token_saving", "telemetry", "auto_approve", "parallel",
    "checkpoint", "mcp", "cost_display", "account_required",
    "target_audience",
]

SCORE_KEYS = [
    "audience", "ui", "learning", "steering",
    "stuck_free", "error_handling", "speed_feel", "overall",
]

REVIEWERS = ["ChatGPT", "Gemini", "Claude", "Devin (SWE-2)"]

RUN_FIELDS = {
    "date": "?", "model": "?", "success": "?", "duration_sec": "?",
    "tokens_in": "?", "tokens_out": "?", "cost_usd": "?",
    "interventions": "?", "diff_url": "?", "notes": "?",
}


def load_editors() -> list[dict]:
    return json.loads((BENCH / "data" / "editors.json").read_text(encoding="utf-8"))["editors"]


def scaffold_results(editor: dict) -> dict:
    runs = []
    for category in editor["categories"]:
        for task in TASKS:
            runs.append({"task": task, "category": category, "run": 1, **RUN_FIELDS})
    return {"editor_id": editor["id"], "runs": runs}


def scaffold_reviews(editor: dict) -> dict:
    return {
        "editor_id": editor["id"],
        "matrix": {k: "?" for k in MATRIX_KEYS},
        "install": {"time_min": "?", "steps": "?", "deps": "?", "hw_spec": "?", "difficulty": "?"},
        "usability_reviews": [
            {
                "reviewer": r,
                "date": "?",
                "version": "?",
                "scores": {k: "?" for k in SCORE_KEYS},
                "comment": "?",
            }
            for r in REVIEWERS
        ],
    }


def main() -> None:
    editors = load_editors()
    for editor in editors:
        for subdir, builder in (("results", scaffold_results), ("reviews", scaffold_reviews)):
            path = BENCH / subdir / f"{editor['id']}.json"
            if path.exists():
                print(f"skip (exists): {path.name}")
                continue
            path.write_text(
                json.dumps(builder(editor), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"created: {subdir}/{path.name}")


if __name__ == "__main__":
    main()
