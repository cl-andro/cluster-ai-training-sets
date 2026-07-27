---
language:
- en
base_model: unsloth/Qwen2.5-Coder-0.5B-Instruct
pipeline_tag: text-generation
tags:
- gguf
- llama.cpp
- unsloth
- linux
- bash
- devops
- slm
license: other
---

# Cluster Worker v2 0.5B GGUF

> **This is a trailer — contact for the fully upgraded version with enhanced fine-tuning and extended coverage.**
>
> **Need a custom model for your specific task? Reach out for tailored fine-tuning.**

**Cluster Worker v2** is a highly specialized Small Language Model (SLM) fine-tuned on **65,000+ Linux & DevOps task samples**. It is engineered specifically to act as a **deterministic, zero-fluff CLI execution worker** inside dual-agent AI architectures.

Unlike standard chat models, this model uses **response-only loss masking** to completely eliminate conversational filler, explanations, and unnecessary Markdown wrappers — returning strictly valid, executable Bash commands.

---

## Licensing & Commercial Use

This model is released under the **Business Source License 1.1 (BSL 1.1)**. 
- **Free Use:** Free for non-production, testing, academic, and evaluation purposes.
- **Commercial Use:** If you wish to use this model in production for commercial purposes, applications, or enterprise services, you **must acquire a commercial license**.

### Contact for Enterprise Licensing
For production keys, custom fine-tuning on your company data, or commercial licensing inquiries, please reach out directly:
- **Email:** mohammadzaidkhanofficial@gmail.com
- **LinkedIn:** [https://www.linkedin.com/in/mohammad-zaid-5021ab3b1](https://www.linkedin.com/in/mohammad-zaid-5021ab3b1)

---

## Key Features

- **Zero Conversational Fluff:** No *"Sure, here is your command:"* or introductory text. It outputs raw code meant directly for stdout/terminal execution.
- **Enterprise Sysadmin Coverage:** Fine-tuned on multi-step Linux administrative tasks, file system manipulation, log parsing (`awk`, `grep`, `sed`), networking, and systemd management.
- **Ultra-Low Footprint:** Built on `Qwen2.5-Coder-0.5B-Instruct` and quantized to **Q8_0**, taking up under **600 MB of VRAM/RAM**.
- **Optimized for Dual-Agent Architectures:** Serves as a zero-cloud-token execution node when paired with primary reasoning models (e.g., Gemini, Claude, GPT-4o, or a 7B Architect model).

---

---

## Quickstart & Deployment

### Method 1: Automated Script (Recommended)

If using Debian/Ubuntu Linux, run the official automated setup script to install Ollama, build the local wrapper, and launch the worker:

```bash
curl -fsSL https://raw.githubusercontent.com/cl-andro/cluster-ai-training-sets/main/cluster-worker-nonthink-ai.sh | bash
```

---

### Method 2: Ollama (`Modelfile`)

You can run this model directly in [Ollama](https://ollama.com/) using the ChatML standard format.

1. Create a file named `Modelfile`:

```dockerfile
FROM hf.co/zk-mohammad/cluster-worker-v2-0.5b-GGUF

TEMPLATE """<|im_start|>system
You are a strict, zero-fluff Linux terminal worker. Return strictly the bash command, no explanations, no markdown chat, no formatting.<|im_end|>
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""

PARAMETER temperature 0.0
PARAMETER top_k 1
PARAMETER stop "<|im_end|>"
PARAMETER stop "<|im_start|>"
```

2. Build and run the model:

```bash
ollama create worker -f Modelfile
ollama run worker "Find all files ending in .log in /var/log older than 7 days and delete them."
```

---

### Method 3: `llama.cpp` CLI

Run directly via `llama-cli` with Jinja template support enabled:

```bash
llama-cli -hf zk-mohammad/cluster-worker-v2-0.5b-GGUF \
  --jinja \
  --temp 0.0 \
  -p "Find all files ending in .log in /var/log older than 7 days and delete them."
```

---

## Example Outputs

| User Request | Worker Model Output |
| --- | --- |
| *Find all .log files in /var/log older than 7 days and delete them.* | `find /var/log -name '*.log' -mtime +7 -delete` |
| *Extract column 1 from access.log, count unique values, and print top 5.* | `awk '{print $1}' access.log \| sort \| uniq -c \| sort -rn \| head -5` |
| *List all hidden files with human-readable file sizes.* | `ls -la` |

---

## Prompt Format (ChatML)

This model follows the standard **Qwen2.5 ChatML** prompt structure:

```text
<|im_start|>system
You are a strict, zero-fluff Linux terminal worker. Return strictly the bash command, no explanations, no markdown chat, no formatting.<|im_end|>
<|im_start|>user
[Your Terminal Task Request]<|im_end|>
<|im_start|>assistant
```

---

## Recommended Inference Parameters

To ensure deterministic execution and prevent conversational drift:

- **Temperature:** `0.0`
- **Top_K:** `1`
- **Sampling:** Disabled (Greedy decoding)

---
