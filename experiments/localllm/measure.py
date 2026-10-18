"""Ollama speed/behavior measurement helper.

Usage:
    python measure.py <model> <prompt_file> <label> [num_predict] [run_tag] [think]

`think` is "false" (default) or an Ollama think level like "low"/"medium"/"high".

Appends one JSON line to bench/results.jsonl and saves the full response to
bench/out/<model>__<label>__<run_tag>.txt
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

OLLAMA_URL = "http://localhost:11434/api/generate"
HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")
OUTDIR = os.path.join(HERE, "out")

NUM_CTX = 4096
NUM_THREAD = 4  # 6C CPU: leave headroom for OS/IDE
TEMPERATURE = 0.2


def run(model: str, prompt: str, num_predict: int, think) -> dict:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": think if think != "false" else False,
        "options": {
            "temperature": TEMPERATURE,
            "num_ctx": NUM_CTX,
            "num_thread": NUM_THREAD,
            "num_predict": num_predict,
        },
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=3600) as r:
            res = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:2000])
        sys.exit(1)
    wall = time.time() - t0

    pe_tok = res.get("prompt_eval_count", 0)
    pe_ns = res.get("prompt_eval_duration", 0)
    e_tok = res.get("eval_count", 0)
    e_ns = res.get("eval_duration", 0)
    return {
        "model": model,
        "prompt_eval_count": pe_tok,
        "prompt_eval_tok_s": round(pe_tok / (pe_ns / 1e9), 2) if pe_ns else None,
        "eval_count": e_tok,
        "eval_tok_s": round(e_tok / (e_ns / 1e9), 2) if e_ns else None,
        "wall_s": round(wall, 1),
        "response": res.get("response", ""),
        "thinking": res.get("thinking", ""),
    }


def main() -> None:
    model, prompt_file, label = sys.argv[1], sys.argv[2], sys.argv[3]
    num_predict = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    run_tag = sys.argv[5] if len(sys.argv) > 5 else "r1"
    think = sys.argv[6] if len(sys.argv) > 6 else "false"

    with open(prompt_file, encoding="utf-8") as f:
        prompt = f.read()

    print(f"[{run_tag}] {model} <- {os.path.basename(prompt_file)} "
          f"(num_predict={num_predict}, think={think}) ...", flush=True)
    out = run(model, prompt, num_predict, think)

    response = out.pop("response")
    thinking = out.pop("thinking")
    safe_model = model.replace(":", "-").replace("/", "-")
    resp_path = os.path.join(OUTDIR, f"{safe_model}__{label}__{run_tag}.txt")
    with open(resp_path, "w", encoding="utf-8") as f:
        if thinking:
            f.write("=== thinking ===\n" + thinking + "\n=== response ===\n")
        f.write(response)

    rec = {"label": label, "run": run_tag, "prompt_file": os.path.basename(prompt_file), **out}
    with open(RESULTS, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(json.dumps({k: v for k, v in rec.items()}, ensure_ascii=False))
    print(f"  response saved -> {resp_path}")


if __name__ == "__main__":
    main()
