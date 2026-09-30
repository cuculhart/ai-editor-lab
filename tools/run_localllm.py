"""CLI 系ツールを Ollama (qwen3.5:4b) でローカルLLMタスクを実行するランナー。

fixture/ をコピーした runs/<tool>/<TASK>/run<N>/ を作業ディレクトリにし、
タスクプロンプトを非対話実行する。標準出力は agent.log に保存。
タイムアウトは plan.md の 15 分上限に合わせ 900 秒。

usage:
  python tools/run_localllm.py goose L1 L2 L3
  python tools/run_localllm.py opencode L2

前提:
  - Ollama が起動し qwen3.5:4b が pull 済み
  - 対象ツールが実行可能（goose: .tools/bin/goose-package/goose.exe、
    opencode: npm グローバル + ~/.config/opencode/opencode.jsonc の
    OpenAI互換 endpoint 設定）
  - localhost が IPv6 で解決されて失敗する環境があるため 127.0.0.1 を使用
    （zoocode L1 の「localhost指定はfetch failed」実績に由来）
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
FIXTURE = BENCH / "fixture"
MODEL = "qwen3.5:4b"
TIMEOUT_SEC = 900

TOOLS = {
    "goose": {
        "exe": str(BENCH / ".tools" / "bin" / "goose-package" / "goose.exe"),
        "args": lambda prompt: [
            "run", "-t", prompt,
            "--provider", "ollama", "--model", MODEL,
            "--with-builtin", "developer",
            "--max-turns", "40", "--no-session",
        ],
        "env": {
            "OLLAMA_HOST": "http://127.0.0.1:11434",
            "GOOSE_MODE": "auto",
        },
    },
    "opencode": {
        "exe": "opencode",
        "args": lambda prompt: ["run", "--model", f"ollama/{MODEL}", prompt],
        "env": {},
    },
}


def find_prompt(task: str) -> Path:
    matches = sorted((BENCH / "tasks").glob(f"{task}-*/prompt.txt"))
    if not matches:
        sys.exit(f"prompt not found: tasks/{task}-*/prompt.txt")
    return matches[0]


def run_task(tool: str, task: str, run_no: int = 1) -> int:
    spec = TOOLS[tool]
    prompt = find_prompt(task).read_text(encoding="utf-8").strip()
    run_dir = BENCH / "runs" / tool / task / f"run{run_no}"
    if run_dir.exists():
        shutil.rmtree(run_dir)
    shutil.copytree(FIXTURE, run_dir, ignore=shutil.ignore_patterns("__pycache__"))

    env = dict(os.environ)
    env.update(spec["env"])
    env["PYTHONUTF8"] = "1"

    log_path = run_dir / "agent.log"
    print(f"[{tool} {task}] start: cwd={run_dir}", flush=True)
    t0 = time.time()
    with open(log_path, "w", encoding="utf-8", errors="replace") as log:
        try:
            proc = subprocess.run(
                [spec["exe"], *spec["args"](prompt)],
                cwd=run_dir, env=env,
                stdout=log, stderr=subprocess.STDOUT,
                timeout=TIMEOUT_SEC,
            )
            elapsed = int(time.time() - t0)
            print(f"[{tool} {task}] done: exit={proc.returncode} {elapsed}s", flush=True)
            return proc.returncode
        except subprocess.TimeoutExpired:
            elapsed = int(time.time() - t0)
            log.write(f"\n=== TIMEOUT {TIMEOUT_SEC}s ===\n")
            print(f"[{tool} {task}] TIMEOUT {elapsed}s", flush=True)
            return 124


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit("usage: python tools/run_localllm.py <tool> <TASK> [<TASK> ...]")
    tool = sys.argv[1]
    if tool not in TOOLS:
        sys.exit(f"unknown tool: {tool} (supported: {', '.join(TOOLS)})")
    for t in sys.argv[2:]:
        run_task(tool, t)


if __name__ == "__main__":
    main()
