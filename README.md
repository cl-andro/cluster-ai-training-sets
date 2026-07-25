# Terminal AI Training Sets

**Curated datasets for fine-tuning LLMs on Linux System Administration, DevOps, and Database Management.**

---

## Overview

This repository contains two datasets:

### 1. `terminal-training-set/` (with thinking reasoning)

**1000** high-quality training entries across 10 categories of real-world system administration scenarios. Each entry includes `<think>` reasoning blocks for chain-of-thought training.

| Category | Entries |
|----------|---------|
| System diagnostics & OOM | 100 |
| systemd service management | 100 |
| Nginx proxy & SSL | 100 |
| Git hooks & secrets | 100 |
| Docker & Compose | 100 |
| Log cleanup & rotation | 100 |
| Network & firewall | 100 |
| Language environments | 100 |
| Users, perms & storage | 100 |
| Database maintenance | 100 |

### 2. `terminal-training-set-nonthinking/` (direct command pairs)

**5000** instruction-output command pairs across 20 categories, designed for training models that output direct Bash commands without reasoning blocks. Each entry is `{"instruction": "...", "output": "..."}` — no conversational filler.

| # | Category | Files | Entries |
|---|----------|-------|---------|
| 01 | File & directory management | 10 | ~250 |
| 02 | Git operations | 10 | ~250 |
| 03 | Package management | 10 | ~250 |
| 04 | Process & service control | 10 | ~250 |
| 05 | System diagnostics & usage | 10 | ~250 |
| 06 | Networking & downloading | 10 | ~250 |
| 07 | Text & file processing | 10 | ~250 |
| 08 | Archiving & compression | 10 | ~250 |
| 09 | Virtual envs & runtimes | 10 | ~250 |
| 10 | Docker & containers | 10 | ~250 |
| 11 | Kubernetes (K8s) | 10 | ~250 |
| 12 | Databases | 10 | ~250 |
| 13 | Security & permissions | 10 | ~250 |
| 14 | Monitoring & alerting | 10 | ~250 |
| 15 | Cloud CLI tools | 10 | ~250 |
| 16 | Shell scripting & automation | 10 | ~250 |
| 17 | System configuration | 10 | ~250 |
| 18 | Performance tuning | 10 | ~250 |
| 19 | Web servers & proxies | 10 | ~250 |
| 20 | SSH & remote access | 10 | ~250 |

### Dataset Structure

```
terminal-training-set/           (10 files: batch1–batch10, 1000 entries)
terminal-training-set-nothinking/ (200 files: 20 categories × 10 batches, 5000 entries)
  ├── 01-file-directory-management.json .. batch-10.json
  ├── 02-git-operations.json          .. batch-10.json
  ├── 03-package-management.json      .. batch-10.json
  ├── 04-process-service-control.json .. batch-10.json
  ├── 05-system-diagnostics-usage.json .. batch-10.json
  ├── 06-networking-downloading.json  .. batch-10.json
  ├── 07-text-file-processing.json    .. batch-10.json
  ├── 08-archiving-compression.json   .. batch-10.json
  ├── 09-virtual-envs-runtimes.json   .. batch-10.json
  ├── 10-docker-container.json        .. batch-10.json
  ├── 11-kubernetes-k8s.json          .. batch-10.json
  ├── 12-databases.json               .. batch-10.json
  ├── 13-security-permissions.json    .. batch-10.json
  ├── 14-monitoring-alerting.json     .. batch-10.json
  ├── 15-cloud-cli-tools.json         .. batch-10.json
  ├── 16-shell-scripting-automation.json .. batch-10.json
  ├── 17-system-configuration.json    .. batch-10.json
  ├── 18-performance-tuning.json      .. batch-10.json
  ├── 19-web-servers-proxies.json     .. batch-10.json
  └── 20-ssh-remote-access.json       .. batch-10.json
```

### Dataset Statistics

#### with-thinking (`terminal-training-set/`)

| Metric | Value |
|--------|-------|
| Total entries | 1000 |
| Total size | ~2.6 MB (JSON) |
| Files | 10 |
| Topics | System diagnostics, services, proxies, git, Docker, logs, networking, languages, permissions, databases |
| Target OS | Linux - Debian 12/13 / Ubuntu 22.04+ |
| Format | JSON with `instruction` + `output` fields |
| Reasoning | Every entry includes `<think>` tags for chain-of-thought |

#### no-thinking (`terminal-training-set-nothinking/`)

| Metric | Value |
|--------|-------|
| Total entries | 5000 |
| Total size | ~948 KB (JSON) |
| Files | 200 |
| Topics | File mgmt, Git, packages, processes, diagnostics, networking, text processing, archiving, virtual envs, Docker, Kubernetes, databases, security, monitoring, cloud CLI, scripting, system config, performance tuning, web servers, SSH |
| Target OS | Linux - Debian 12/13/ Ubuntu 22.04+ |
| Format | JSON with `instruction` + `output` fields |

## Use Cases

- **Fine-tuning language models** for Linux/DevOps assistant capabilities
- **Training thinking models** that reason before acting (chain-of-thought)
- **Training non-thinking models** for direct command output
- **Benchmarking** model performance on structured infrastructure tasks

## Format Examples

### with-thinking format
```json
{
  "instruction": "MySQL keeps crashing on a 64GB RAM server after about 4 hours...",
  "output": "<think>\nThe root cause is almost certainly innodb_buffer_pool_size...\n</think>\n\n```bash\nsudo dmesg | grep -i 'oom-killer' | tail -20\n...\n```"
}
```

### no-thinking format
```json
{"instruction": "List all running services", "output": "systemctl list-units --type=service --state=running"}
```

## Getting Started

```bash
# Quick stats for no-thinking set
python3 -c "
import json, os
for f in sorted(os.listdir('terminal-training-set-nothinking')):
    if f.endswith('.json'):
        with open(f'terminal-training-set-nothinking/{f}') as fp:
            print(f'{f}: {len(json.load(fp))} entries')
"
```

## Licensing

**Proprietary** — Copyright © 2026 Cluster Family / Mohammad Zaid.  
See [LICENSE](LICENSE) for full terms.

For fine-tuning licenses, custom dataset development, or collaboration inquiries,
see [CONTACT.md](CONTACT.md) or email **zkalamgir@proton.me**.
