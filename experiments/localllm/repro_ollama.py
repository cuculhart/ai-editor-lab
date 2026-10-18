"""Reproduce teaspoon-ide's /api/chat request shape for debugging.

Builds the same system prompt (AGENT_SYSTEM_PROMPT + osNote) and user
message ("Context: ... User message: ...") that ollamaService sends,
then reports whether message.content came back empty.
"""

import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "..", "..", "teaspoon-ide")
PROMPT_TS = os.path.join(REPO, "src", "services", "agentPrompt.ts")


def extract_template(src: str, name: str) -> str:
    m = re.search(rf"{name}\s*=\s*`([\s\S]*?)`", src)
    return m.group(1) if m else ""


def main() -> None:
    model = sys.argv[1] if len(sys.argv) > 1 else "gpt-oss:20b"
    user_prompt = sys.argv[2] if len(sys.argv) > 2 else (
        "Which file and which function computes the final price a customer "
        "pays, including the member discount? Look it up in the project, don't guess."
    )
    think = sys.argv[3] if len(sys.argv) > 3 else "low"

    src = open(PROMPT_TS, encoding="utf-8").read()
    sys_prompt = (
        extract_template(src, "APP_CONTEXT_PROMPT") + extract_template(src, "AGENT_INSTRUCTIONS")
    ).strip()
    sys_prompt += '\n\nThe app runs on Windows. To open a file/URL in the browser, emit "// RUN_COMMAND: start <target>".'
    if len(sys.argv) > 4:
        sys_prompt += "\n\n" + sys.argv[4]

    ctx = "Files:\nREADME.md\ncalc.py\ncart.py\nmain.py\ntest_calc.py"
    user = f"Context:\n{ctx}\n\nUser message:\n{user_prompt}"

    messages = [
        {"role": "system", "content": sys_prompt},
    ]
    if len(sys.argv) > 5 and sys.argv[5] == "fewshot":
        messages += [
            {"role": "user", "content": "Show me the file list."},
            {"role": "assistant", "content": "I'll list the files in the project.\n// LIST_FILES: ."},
        ]
    messages.append({"role": "user", "content": user})

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"num_thread": 4, "num_ctx": 8192},
    }
    if think != "unset":
        payload["think"] = think if think != "false" else False

    print(f"model={model} think={think} sys_prompt={len(sys_prompt)} chars")
    req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=3600) as r:
        res = json.loads(r.read())
    msg = res.get("message", {})
    content = msg.get("content", "")
    thinking = msg.get("thinking", "")
    print(f"done_reason={res.get('done_reason')} eval_count={res.get('eval_count')} "
          f"prompt_eval_count={res.get('prompt_eval_count')}")
    print(f"--- thinking ({len(thinking)} chars) ---\n{thinking[:1000]}")
    print(f"--- content ({len(content)} chars) ---\n{content[:2000]}")


if __name__ == "__main__":
    main()
