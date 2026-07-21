# Cluster AI Training Sets

**Proprietary curated datasets for fine-tuning LLMs on Linux System Administration, DevOps, and Database Management.**

---

## Overview

This repository contains 987 high-quality training entries across 10 categories of real-world system administration scenarios. Each entry consists of:

- **`instruction`** — A realistic, detailed problem statement or task request
- **`output`** — A structured response with:
  - `<think>` reasoning block (chain-of-thought analysis)
  - ````bash` executable code block (production-grade bash for Debian 12 / Ubuntu)

### Dataset Structure

```
terminal-training-set/
├── batch1_system_diagnostics_oom.json          # 100 entries — OOM diagnostics, memory tuning
├── batch2_systemd_services.json                # 100 entries — systemd unit management
├── batch3_nginx_proxy.json                     # 100 entries — nginx reverse proxy, SSL, caching
├── batch4_git_security_hooks.json              # 100 entries — git hooks, secret scanning
├── batch5_docker.json                          # 100 entries — Dockerfiles, Compose, registries
├── batch6_log_cleanup.json                     # 100 entries — logrotate, journald, audit
├── batch7_network_ports_firewall.json          # 100 entries — nftables, iptables, port scanning
├── batch8_language_environments.json           #  87 entries — Python, Node.js, Go, Rust setup
├── batch9_user_permissions_storage.json        # 100 entries — ACLs, quotas, LUKS, sudoers
└── batch10_database_maintenance_backups.json   # 100 entries — PostgreSQL, MySQL, MongoDB, backup
```

### Dataset Statistics

| Metric | Value |
|--------|-------|
| Total entries | 987 |
| Total size | ~2.6 MB (JSON) |
| Files | 10 |
| Topics | System diagnostics, services, proxies, git, Docker, logs, networking, languages, permissions, databases |
| Target OS | Debian 12 / Ubuntu 22.04+ |
| Format | JSON with `instruction` + `output` fields |
| Reasoning | Every entry includes `<think>` tags for chain-of-thought |

## Use Cases

- **Fine-tuning language models** for Linux/DevOps assistant capabilities
- **Training thinking models** that reason before acting (chain-of-thought)
- **Training non-thinking models** by stripping `<think>` tags for direct response
- **Benchmarking** model performance on structured infrastructure tasks

## Format Example

```json
{
  "instruction": "MySQL keeps crashing on a 64GB RAM server after about 4 hours...",
  "output": "<think>\nThe root cause is almost certainly innodb_buffer_pool_size...\n</think>\n\n```bash\nsudo dmesg | grep -i 'oom-killer' | tail -20\n...\n```"
}
```

## Getting Started

```bash
# Clone
git clone git@github-third:cl-andro/cluster-ai-training-sets.git
cd cluster-ai-training-sets

# Quick stats
python3 -c "
import json, os
for f in sorted(os.listdir('terminal-training-set')):
    with open(f'terminal-training-set/{f}') as fp:
        print(f'{f}: {len(json.load(fp))} entries')
"
```

## Licensing

**Proprietary** — Copyright © 2026 Cluster Family / Mohammad Zaid.  
See [LICENSE](LICENSE) for full terms.

For fine-tuning licenses, custom dataset development, or collaboration inquiries,
see [CONTACT.md](CONTACT.md) or email **zaidkhanalamgir01@gmail.com**.
