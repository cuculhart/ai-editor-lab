"""Teaspoon IDE v0.9.1 の auto_summarize フラグ ON/OFF 比較テスト。

compactHistory はターン完了後にのみ走り、発火条件は未要約メッセージ
30件超(SUMMARY_TRIGGER)。単発タスクでは届かないため、1会話内で
T1→T2→T3 を連続実行して会話を積み上げ、最後に「最初の指示を復唱」
するプローブを送る。

- OFF: HISTORY_WINDOW=20 を超えた先頭は切り捨て + 注記のみ
- ON : 先頭が1500字以内の要約として注入される

観測指標:
- chat_conversations の summarizedCount/contextSummary（要約が実際に
  発火したかの直接証拠）
- プローブ応答が T1 の仕様（割引境界値 quantity>=3 / TestCart）を
  正しく想起できるか
- 最終 accept.py 結果（参考）

usage:
  python tools/test_summarize_flag.py on|off [run_no]

出力先: bench/tmp/summarize-test/<flag>-run<N>/
"""
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

BENCH = Path(__file__).resolve().parents[1]
EXE = (BENCH.parent / "teaspoon-ide" / "out" / "Teaspoon-0.9.1"
       / "Teaspoon-win32-x64" / "Teaspoon.exe")
FIXTURE = BENCH / "fixture"
OUT = BENCH / "tmp" / "summarize-test"
GEMINI_MODEL = "gemini-3.5-flash-lite"
GEMINI_KEY_FILE = BENCH / ".secrets" / "gemini-key.txt"
TURN_TIMEOUT = 600
POLL_SEC = 2

TURNS = [
    ("T1", (BENCH / "tasks" / "T1-bugfix" / "prompt.txt")
        .read_text(encoding="utf-8").strip()),
    ("T2", (BENCH / "tasks" / "T2-feature" / "prompt.txt")
        .read_text(encoding="utf-8").strip()),
    ("T4", (BENCH / "tasks" / "T4-testgen" / "prompt.txt")
        .read_text(encoding="utf-8").strip()),
    ("T5", (BENCH / "tasks" / "T5-docs" / "prompt.txt")
        .read_text(encoding="utf-8").strip()),
    ("T6", (BENCH / "tasks" / "T6-webapp" / "prompt.txt")
        .read_text(encoding="utf-8").strip()),
    ("T3", (BENCH / "tasks" / "T3-refactor" / "prompt.txt")
        .read_text(encoding="utf-8").strip()),
    ("probe",
     "この会話で私が最初にお願いしたタスクは何でしたか？"
     "最初の指示文に書かれていた、修正すべき具体的な内容を復唱してください。"),
]
ACCEPT = BENCH / "tasks" / "T3-refactor" / "accept.py"


def wait_idle(page, log, interventions: list) -> int:
    t0 = time.time()
    idle_polls = 0
    while True:
        if time.time() - t0 > TURN_TIMEOUT:
            log(f"TURN TIMEOUT after {TURN_TIMEOUT}s")
            return int(time.time() - t0)
        try:
            approve = page.query_selector(
                ".file-edit-approval .approve-button")
            if approve and approve.is_visible():
                approve.click()
                interventions[0] += 1
                log(f"approved edit (#{interventions[0]})")
                continue
        except Exception:
            pass
        busy = page.query_selector(".cancel-button")
        disabled = page.get_attribute(".chat-input textarea", "disabled")
        if busy is None and disabled is None:
            idle_polls += 1
            if idle_polls >= 3:
                return int(time.time() - t0)
        else:
            idle_polls = 0
        time.sleep(POLL_SEC)


def run_accept(workdir: Path) -> bool:
    r = subprocess.run(
        [sys.executable, str(ACCEPT), str(workdir)],
        capture_output=True, encoding="utf-8", errors="replace", timeout=120,
    )
    return r.returncode == 0


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("on", "off"):
        sys.exit("usage: python tools/test_summarize_flag.py on|off [run_no]")
    flag = sys.argv[1]
    run_no = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    run_dir = OUT / f"{flag}-run{run_no}"
    if run_dir.exists():
        shutil.rmtree(run_dir)
    shutil.copytree(FIXTURE, run_dir, ignore=shutil.ignore_patterns("__pycache__"))

    log_lines: list[str] = []

    def log(msg: str) -> None:
        line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        log_lines.append(line)

    key = GEMINI_KEY_FILE.read_text(encoding="utf-8").strip()
    interventions = [0]
    port = 9222

    with sync_playwright() as p:
        env = os.environ.copy()
        env.pop("ELECTRON_RUN_AS_NODE", None)
        proc = subprocess.Popen(
            [str(EXE), f"--remote-debugging-port={port}", str(run_dir)],
            env=env,
        )
        browser = None
        for _ in range(60):
            try:
                browser = p.chromium.connect_over_cdp(
                    f"http://127.0.0.1:{port}")
                break
            except Exception:
                time.sleep(1)
        if browser is None:
            proc.kill()
            raise RuntimeError("CDP connect failed")
        page = None
        for _ in range(60):
            for ctx in browser.contexts:
                for pg in ctx.pages:
                    if not pg.url.startswith(
                            ("devtools://", "chrome-", "about:")):
                        page = pg
                        break
                if page:
                    break
            if page:
                break
            time.sleep(1)
        if page is None:
            proc.kill()
            raise RuntimeError("app page not found")
        page.set_default_timeout(15_000)
        log("app launched (v0.9.1)")

        page.evaluate(
            """([model, key, summarize]) => {
                localStorage.setItem('llm_provider', 'gemini')
                localStorage.setItem('gemini_api_key', key)
                localStorage.setItem('gemini_model', model)
                localStorage.setItem('auto_summarize', summarize)
                localStorage.removeItem('chat_conversations')
            }""",
            [GEMINI_MODEL, key, "1" if flag == "on" else "0"],
        )
        try:
            page.reload(wait_until="domcontentloaded")
        except Exception:
            pass
        page.wait_for_selector(
            ".chat-input textarea:not([disabled])", state="visible")
        log(f"configured: gemini auto_summarize={flag}")

        for name, prompt in TURNS:
            page.fill(".chat-input textarea", prompt)
            page.click(".send-button")
            log(f"{name} sent")
            dur = wait_idle(page, log, interventions)
            log(f"{name} done in {dur}s")

        a = run_accept(run_dir)
        log(f"accept (T3) at end: {'PASS' if a else 'FAIL'}")
        log(f"total interventions={interventions[0]}")

        try:
            texts = page.eval_on_selector_all(
                ".chat-message .message-text",
                "els => els.map(e => e.innerText)")
            log_lines.append("\n=== chat messages ===")
            log_lines.extend(texts)
            log(f"chat messages: {len(texts)}")
        except Exception as e:
            log(f"chat dump failed: {e}")
        page.screenshot(path=str(run_dir / "screenshot.png"), full_page=True)
        proc.terminate()

    # 要約が実際に発火したかの直接証拠。会話は
    # %APPDATA%/Teaspoon/chat-history/conv_*.json に保存される。
    # 直近に更新されたものが今回の会話。
    try:
        import glob as _glob
        hist = Path(os.environ["APPDATA"]) / "Teaspoon" / "chat-history"
        files = sorted(_glob.glob(str(hist / "conv_*.json")),
                       key=os.path.getmtime)
        conv = json.loads(Path(files[-1]).read_text(encoding="utf-8"))
        log(f"conversation msgs={len(conv.get('messages') or [])} "
            f"summarizedCount={conv.get('summarizedCount')} "
            f"summary_len={len(conv.get('contextSummary') or '')}")
        if conv.get("contextSummary"):
            log_lines.append("=== contextSummary ===")
            log_lines.append(conv["contextSummary"])
    except Exception as e:
        log(f"summary state read failed: {e}")

    (run_dir / "agent.log").write_text("\n".join(log_lines), encoding="utf-8")
    print(f"saved -> {run_dir}")


if __name__ == "__main__":
    main()
