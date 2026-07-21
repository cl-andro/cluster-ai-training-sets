# Dataset Card — Cluster AI Terminal Training Sets

## Description

Curated dataset of 987 real-world Linux System Administration / DevOps scenarios with chain-of-thought reasoning and executable bash solutions. Designed for fine-tuning language models to act as expert system administrators.

## Composition

- **Languages:** 100% English
- **Format:** JSON (`instruction` + `output` with `<think>` and ````bash` blocks)
- **License:** Proprietary (see [LICENSE](../LICENSE))

## Categories

| # | Category | Entries |
|---|----------|---------|
| 1 | System Diagnostics & OOM | 100 |
| 2 | systemd Services | 100 |
| 3 | nginx Proxy & SSL | 100 |
| 4 | Git Security Hooks | 100 |
| 5 | Docker & Containers | 100 |
| 6 | Log Cleanup & Rotation | 100 |
| 7 | Network Ports & Firewall | 100 |
| 8 | Language Environments | 87 |
| 9 | User Permissions & Storage | 100 |
| 10 | Database Maintenance & Backups | 100 |

## Intended Use

- Fine-tuning instruct models for Linux/DevOps Q&A
- Chain-of-thought reasoning model training
- Benchmarking structured task completion

## Limitations

- Debian 12 / Ubuntu 22.04 focused (not RHEL, Arch, etc.)
- Shell-only tasks (no Python automation libraries like Fabric/Ansible)
- Batch 8 is 87/100 entries (in progress)

## Contact

Mohammad Zaid — zaidkhanalamgir01@gmail.com
