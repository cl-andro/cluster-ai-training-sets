# Terminal AI Training Sets

**Curated datasets for fine-tuning LLMs on Linux System Administration, DevOps, and Database Management.**

---

## Overview

This repository contains two datasets:

### 1. `terminal-training-set/` (with thinking reasoning)

**1000** high-quality training entries across 10 categories of real-world system administration scenarios. Each entry includes `<think>` reasoning blocks.

### 2. `terminal-training-set-nothinking/` (direct command pairs)

**~14,600** instruction-output command pairs across **61 categories**, designed for training models that output direct Bash commands. Each entry is `{"instruction": "...", "output": "..."}` — no conversational filler.

### Dataset Structure

```
terminal-training-set/               (10 files, 1000 entries)
terminal-training-set-nothinking/    (610 files, ~14,600 entries)
  ├── part1/   (categories 01–10)   100 files
  ├── part2/   (categories 11–20)   100 files
  ├── part3/   (category 21)         10 files
  ├── part4/   (categories 22–41)   200 files
  └── part5/   (categories 42–61)   200 files
```

### Dataset Statistics

#### with-thinking (`terminal-training-set/`)

| Metric | Value |
|--------|-------|
| Total entries | 1000 |
| Total size | ~2.6 MB |
| Files | 10 |
| Categories | 10 |
| Target OS | Debian 12 / Ubuntu 22.04+ |
| Format | JSON with `instruction` + `output` (+ `<think>` tags) |

#### no-thinking (`terminal-training-set-nothinking/`)

| Metric | Value |
|--------|-------|
| Total entries | ~14,600 |
| Total size | ~3.5 MB |
| Files | 610 |
| Categories | 61 |
| Target OS | Debian 12 |
| Format | JSON with `instruction` + `output` (plain command pairs) |

### All 61 Categories

| # | Folder | Category | Files | ~Entries |
|---|--------|----------|-------|----------|
| 01 | part1/ | File & directory management | 10 | 250 |
| 02 | part1/ | Git operations | 10 | 250 |
| 03 | part1/ | Package management | 10 | 250 |
| 04 | part1/ | Process & service control | 10 | 250 |
| 05 | part1/ | System diagnostics & usage | 10 | 250 |
| 06 | part1/ | Networking & downloading | 10 | 250 |
| 07 | part1/ | Text & file processing | 10 | 250 |
| 08 | part1/ | Archiving & compression | 10 | 250 |
| 09 | part1/ | Virtual envs & runtimes | 10 | 250 |
| 10 | part1/ | Docker & containers | 10 | 250 |
| 11 | part2/ | Kubernetes (K8s) | 10 | 250 |
| 12 | part2/ | Databases | 10 | 250 |
| 13 | part2/ | Security & permissions | 10 | 250 |
| 14 | part2/ | Monitoring & alerting | 10 | 250 |
| 15 | part2/ | Cloud CLI tools | 10 | 250 |
| 16 | part2/ | Shell scripting & automation | 10 | 250 |
| 17 | part2/ | System configuration | 10 | 250 |
| 18 | part2/ | Performance tuning | 10 | 250 |
| 19 | part2/ | Web servers & proxies | 10 | 250 |
| 20 | part2/ | SSH & remote access | 10 | 250 |
| 21 | part3/ | Contrastive edge cases | 10 | 251 |
| 22 | part4/ | systemd deep dive | 10 | 250 |
| 23 | part4/ | Network troubleshooting | 10 | 250 |
| 24 | part4/ | Backup & recovery | 10 | 250 |
| 25 | part4/ | CI/CD pipelines | 10 | 250 |
| 26 | part4/ | Infrastructure as Code | 10 | 250 |
| 27 | part4/ | Log management | 10 | 250 |
| 28 | part4/ | Storage & filesystem | 10 | 250 |
| 29 | part4/ | Kernel & hardware | 10 | 250 |
| 30 | part4/ | Secret management | 10 | 250 |
| 31 | part4/ | DNS & domain | 10 | 250 |
| 32 | part4/ | Email servers | 10 | 250 |
| 33 | part4/ | Certificate management | 10 | 250 |
| 34 | part4/ | API gateways | 10 | 250 |
| 35 | part4/ | Message queues | 10 | 250 |
| 36 | part4/ | Load balancing | 10 | 250 |
| 37 | part4/ | Service mesh | 10 | 250 |
| 38 | part4/ | Package building | 10 | 250 |
| 39 | part4/ | Container registries | 10 | 250 |
| 40 | part4/ | Storage LVM/ZFS | 10 | 250 |
| 41 | part4/ | VPN & tunneling | 10 | 250 |
| 42 | part5/ | Hardware diagnostics & stress | 10 | 250 |
| 43 | part5/ | Desktop & display | 10 | 250 |
| 44 | part5/ | Time synchronization | 10 | 250 |
| 45 | part5/ | Fonts & localization | 10 | 250 |
| 46 | part5/ | Printing (CUPS) | 10 | 250 |
| 47 | part5/ | Audio (PulseAudio/PipeWire) | 10 | 250 |
| 48 | part5/ | Bluetooth | 10 | 250 |
| 49 | part5/ | Power management | 10 | 250 |
| 50 | part5/ | Filesystem mount & automount | 10 | 250 |
| 51 | part5/ | Container orchestration | 10 | 250 |
| 52 | part5/ | Service discovery | 10 | 250 |
| 53 | part5/ | API clients | 10 | 250 |
| 54 | part5/ | Data serialization | 10 | 250 |
| 55 | part5/ | File transfer deep | 10 | 250 |
| 56 | part5/ | Terminal multiplexers | 10 | 250 |
| 57 | part5/ | System rescue & recovery | 10 | 250 |
| 58 | part5/ | Disk cloning & imaging | 10 | 250 |
| 59 | part5/ | Binary analysis | 10 | 250 |
| 60 | part5/ | Process debugging | 10 | 250 |
| 61 | part5/ | USB debugging / ADB | 10 | 250 |

## Use Cases

- Fine-tuning language models for Linux/DevOps assistant capabilities
- Training thinking models that reason before acting (chain-of-thought)
- Training non-thinking models for direct command output
- Benchmarking model performance on structured infrastructure tasks

## Format Example

```json
{"instruction": "List all running services", "output": "systemctl list-units --type=service --state=running"}
```

## Getting Started

```bash
# Quick stats
python3 -c "
import json, os
d = 'terminal-training-set-nothinking'
total = sum(len(json.load(open(os.path.join(d, f)))) for _,_,fs in os.walk(d) for f in fs if f.endswith('.json'))
print(f'Total: {total} entries')
"
```

## Licensing

**Proprietary** — Copyright © 2026 Cluster Family / Mohammad Zaid.
