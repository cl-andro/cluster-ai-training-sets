# Hybrid Agent Architecture: Saving Cloud Tokens with Local SLM Workers

This guide explains how to pair high-level cloud models (such as **Google Gemini 1.5/2.0**, **Claude 3.5 Sonnet**, or **GPT-4o**) with your local **0.5B Worker SLM** to build a hybrid agentic pipeline.

By offloading repetitive, syntax-heavy Bash command generation to a local zero-token model, you can reduce cloud API costs by **70% to 85%** while increasing execution speed.

---

## Architecture Overview

In a traditional agentic workflow, every single reasoning step, command draft, and syntax correction is sent to a cloud model. This burns through context windows and API tokens rapidly.

In a **Hybrid Dual-Agent System**:
1. **Cloud Architect (Gemini / Claude / GPT):** Handles multi-step logic, strategic decision-making, and user interaction.
2. **Local Worker (`worker` / Ollama):** Receives structured step instructions and generates deterministic, zero-fluff Bash commands locally at **$0.00 token cost**.

```
                       +------------------------+
                       |       User Prompt      |
                       +-----------+------------+
                                   |
                                   v
                       +------------------------+
                       |     Cloud Architect    |
                       |   (Gemini / Claude)    |
                       |  High-Level Planning   |
                       +-----------+------------+
                                   |
                 Delegates CLI task| (0 Cloud Tokens)
                                   v
                       +------------------------+
                       |   Local Ollama Worker  |
                       |    Model: "worker"     |
                       |   (0.5B Deterministic) |
                       +-----------+------------+
                                   |
                       Returns raw | stdout command
                                   v
                       +------------------------+
                       |  Target Linux System   |
                       |   (Debian / Terminal)  |
                       +------------------------+
```

---

## Token Cost Comparison

| Workflow Step | Full Cloud Execution | Hybrid Architecture |
| :--- | :--- | :--- |
| **High-level Task Decomposition** | Cloud Tokens | Cloud Tokens |
| **Drafting Terminal Commands** | Cloud Tokens ($$$) | **0 Tokens (Local SLM)** |
| **Command Retries / Syntax Tweaks** | Cloud Tokens ($$$) | **0 Tokens (Local SLM)** |
| **Output Parsing / Verification** | Cloud Tokens | Cloud Tokens |
| **Average Monthly Cost Savings** | **0% Baseline** | **70% – 85% Saved** |

---

## Python Integration Example (Gemini + Local Ollama Worker)

Here is a complete Python script demonstrating how to use Google Gemini as the Primary Architect that delegates execution tasks to your local Ollama `worker`.

### 1. Requirements

```bash
pip install google-genai requests
```

### 2. `hybrid_agent.py`

```python
import os
import requests
from google import genai
from google.genai import types

# 1. Initialize Gemini Client (Cloud Architect)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Local Worker Tool Definition
def generate_local_bash_command(task_description: str) -> str:
    """
    Delegates CLI generation to the local 0.5B Worker running inside Ollama.
    Cost: 0 Cloud Tokens.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "worker",
        "prompt": task_description,
        "stream": False,
        "options": {
            "temperature": 0.0
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        command = response.json().get("response", "").strip()
        return command
    except Exception as e:
        return f"Error contacting local worker: {str(e)}"

# 3. Define Tool Schema for Gemini Function Calling
local_worker_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="generate_local_bash_command",
            description="Generates an exact, zero-fluff Linux terminal command using the local 0.5B worker. Use this whenever you need to execute a command on the terminal.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "task_description": types.Schema(
                        type="STRING",
                        description="Specific terminal request (e.g. 'Find all .log files older than 7 days in /var/log and delete them')"
                    )
                },
                required=["task_description"]
            )
        )
    ]
)

# 4. Agent Execution Loop
def run_hybrid_agent(user_request: str):
    print(f"\n[User Request]: {user_request}")

    # Send request to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_request,
        config=types.GenerateContentConfig(
            tools=[local_worker_tool],
            system_instruction="You are a system architect. Break down user goals and use 'generate_local_bash_command' to obtain terminal commands."
        )
    )

    # Check if Gemini wants to call our local worker tool
    if response.function_calls:
        for call in response.function_calls:
            if call.name == "generate_local_bash_command":
                task = call.args["task_description"]
                print(f"[Gemini Architect]: Delegating task to local worker -> '{task}'")

                # Execute tool locally with 0 cloud tokens
                local_cmd = generate_local_bash_command(task)
                print(f"[Local 0.5B Worker Output]: {local_cmd}")

                # Hand result back to Gemini
                final_response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        types.Content(role="user", parts=[types.Part.from_text(text=user_request)]),
                        types.Content(role="model", parts=response.candidates[0].content.parts),
                        types.Content(
                            role="user",
                            parts=[types.Part.from_function_response(
                                name="generate_local_bash_command",
                                response={"result": local_cmd}
                            )]
                        )
                    ]
                )
                print(f"[Gemini Final Summary]: {final_response.text}")
    else:
        print(f"[Gemini Response]: {response.text}")

if __name__ == "__main__":
    run_hybrid_agent("I need to clean up old log files in /var/log to free up disk space.")
```

---

## Benefits

1. **Zero-Token Overhead:** Repetitive terminal drafting runs on your local GPU/CPU.
2. **Deterministic Output:** Local `worker` uses `temperature 0.0` and `top_k 1` to output pure code without Markdown chatter.
3. **Privacy & Offline Resilience:** Local commands are formed without sending file system metadata or system structures back to cloud API providers.

---

# Integrating Local Worker with OpenCode, Aider, and Agentic Coding Tools

Once installed via `cluster-worker-nonthink-ai.sh`, your local **0.5B Worker** exposes an **OpenAI-Compatible REST API** at:

```
http://localhost:11434/v1
```

You can configure developer tools, coding agents, and terminal assistants (such as **OpenCode**, **Aider**, **Continue.dev**, **Cursor**, or **AutoGen**) to delegate sub-agent tasks directly to this local endpoint.

---

## 1. Quick Setup: Environment Variables

For standard CLI coding tools that read `OPENAI_API_BASE`, set these environment variables in your `~/.bashrc` or terminal session:

```bash
export OPENAI_API_BASE="http://localhost:11434/v1"
export OPENAI_API_KEY="ollama"
export WORKER_MODEL="worker"
```

---

## 2. Integration with OpenCode / Agent Frameworks

To use `worker` as a sub-agent execution provider inside **OpenCode** or similar agent setups, add the local endpoint to your configuration file.

### Example `opencode.json` Configuration:

```json
{
  "sub_agents": {
    "terminal_executor": {
      "provider": "openai",
      "api_base": "http://localhost:11434/v1",
      "api_key": "ollama",
      "model": "worker",
      "temperature": 0.0,
      "system_prompt": "You are a strict, zero-fluff Linux terminal worker. Return strictly the bash command, no explanations, no markdown chat, no formatting."
    }
  },
  "primary_agent": {
    "provider": "anthropic",
    "model": "claude-3-5-sonnet-20241022"
  }
}
```

---

## 3. Python OpenAI SDK Integration

If you use the standard `openai` Python SDK in your projects, point it to your local Ollama port:

```python
from openai import OpenAI

# Connect to local Ollama worker
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Required by SDK, value is ignored by Ollama
)

response = client.chat.completions.create(
    model="worker",
    messages=[
        {"role": "system", "content": "You are a strict, zero-fluff Linux terminal worker."},
        {"role": "user", "content": "Extract column 1 from access.log, count unique values, and print top 5."}
    ],
    temperature=0.0
)

command = response.choices[0].message.content.strip()
print(f"Generated Command: {command}")
```

---

## 4. Continue.dev VS Code Extension Setup

To use `worker` as a quick shell command generator in VS Code via **Continue.dev**, add this entry to your `~/.continue/config.json`:

```json
{
  "models": [
    {
      "title": "Local Terminal Worker (0.5B)",
      "provider": "ollama",
      "model": "worker",
      "apiBase": "http://localhost:11434",
      "systemMessage": "You are a strict, zero-fluff Linux terminal worker. Return strictly the bash command."
    }
  ]
}
```

---

## 5. Aider CLI Setup

To run Aider with your local worker handling terminal operations:

```bash
aider --openai-api-base http://localhost:11434/v1 --openai-api-key ollama --model openai/worker
```

---

## Best Practices & Execution Safety

1. **Keep Temperature at 0.0:** Ensures command generation remains strictly deterministic.
2. **Dry-Run Validation:** When building custom agent wrappers, always print or inspect the command returned by `worker` before passing it to `subprocess.run()`.
3. **Combine Strengths:** Use cloud models for high-level logic (planning, debugging error logs, writing architecture docs) and the local worker for simple execution syntax (`find`, `awk`, `grep`, `tar`, `systemctl`).
