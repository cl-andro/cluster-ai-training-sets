# Terminal AI Training Sets

**Curated datasets for fine-tuning LLMs on Linux System Administration, DevOps, and Database Management.**

---

## Overview

This repository contains two datasets:

### 1. `terminal-training-set/` (with thinking reasoning)

**66,463** trainable entries — 2,810 files across 280 categories. Each entry includes a `<think>` reasoning block followed by the exact executable command. Think blocks provide task breakdown, tool selection logic, and safety/edge-case analysis.

### 2. `terminal-training-set-nothinking/` (direct command pairs)

**65,463** instruction-output command pairs across **280 categories**, designed for training models that output direct Bash commands. Each entry is `{"instruction": "How to ...", "output": "bare command"}` — no conversational filler, no markdown, no explanations.

### Dataset Structure

```
terminal-training-set/               (2,810 files, 66,463 entries — think blocks)
terminal-training-set-nothinking/    (2,800 files, 65,463 entries — bare commands)
  ├── part1/   (categories 01–10)     100 files
  ├── part2/   (categories 11–20)     100 files
  ├── part3/   (category 21)           10 files
  ├── part4/   (categories 22–41)     200 files
  ├── part5/   (categories 42–61)     200 files
  ├── part6/   (categories 62–95)     340 files
  ├── part7/   (categories 96–105)    100 files
  ├── part8/   (categories 106–116)   110 files
  ├── part9/   (categories 117–136)   200 files
  ├── part10/  (categories 137–176)   400 files
  ├── part11/  (categories 177–186)   100 files
  ├── part12/  (categories 187–196)   100 files
  ├── part13/  (categories 197–206)   100 files
  ├── part14/  (categories 207–216)   100 files
  ├── part15/  (categories 217–226)   100 files
  ├── part16/  (categories 227–236)   100 files
  ├── part17/  (categories 237–246)   100 files
  ├── part18/  (categories 247–256)   100 files
  ├── part19/  (categories 257–266)   100 files
  ├── part20/  (categories 267–276)   100 files
  └── part21/  (categories 277–280)    40 files
```

### Dataset Statistics

#### with-thinking (`terminal-training-set/`)

| Metric | Value |
|--------|-------|
| Total entries | 66,463 |
| Total size | ~32 MB |
| Files | 2,810 |
| Categories | 280 |
| Target OS | Debian 12 / Ubuntu 22.04+ |
| Format | `{"instruction": "...", "output": "<think>...</think>\\n[command]"}` |

#### no-thinking (`terminal-training-set-nothinking/`)

| Metric | Value |
|--------|-------|
| Total entries | **65,463** |
| Total size | ~8.4 MB |
| Files | **2,800** (10 per category) |
| Categories | **280** |
| Format | JSON with `instruction` + `output` (plain command pairs) |
| Entries per file | 20-26 |
| Quality | Output validated — bare commands only, no prompts/explanation |

### Coverage Areas

- **01-10**: File management, Git, packages, processes, networking, archiving, Docker
- **11-21**: K8s, databases, security, monitoring, cloud CLI, scripting, config, tuning
- **22-41**: systemd, networking, backup, CI/CD, IaC, logs, storage, kernel, secrets, DNS, email, certs, API gateways, message queues, load balancing, service mesh, packaging, registries, LVM/ZFS, VPN
- **42-61**: Hardware, display, time, fonts, printing, audio, Bluetooth, power, mounts, orchestration, service discovery, API clients, serialization, file transfer, tmux, rescue, cloning, binary analysis, debugging, ADB
- **62-95**: Python (pip/poetry/conda), Node (npm/yarn/pnpm), Rust/Cargo, Go, C/C++ toolchains, tmux/screen, SSH config, rsync/SSHFS, Mosh, socat/ncat, netcat, tcpdump, Wireshark/tshark, curl/wget, HTTPie, jq, yq, XML/CSV, sed, awk, perf/bench, stress-ng, fio, iperf3, sysbench, LACP/bonding, bridge, VXLAN, VLAN, BGP, WireGuard, OpenVPN, IPSec, HAProxy, nftables/iptables, conntrack, tc, tcpdump analysis, Wireshark CLI, dpkt/scapy, ntopng, Caddy
- **96-105**: Ansible, Terraform/OpenTofu, Pulumi, Packer, Vagrant, Podman, Docker Compose, GitHub CLI, Drone/Woodpecker, Prometheus
- **106-116**: Grafana, Loki, Datadog, OpenTelemetry, iptables/nftables, firewalld, SELinux, AppArmor, auditd, WireGuard, Dockerfile/BuildKit
- **117-136**: kubectl, Helm, Kustomize, containerd/nerdctl, Istio, PostgreSQL, MySQL, SQLite, MongoDB, Elasticsearch, Redis, DB migration, DB benchmarking, Java/JVM, Ruby, PHP, .NET, shell scripting, Make, task runners
- **137-146**: nmap, vulnerability scanning, web app security, password cracking, OSINT, malware analysis, YARA, forensics, rsyslog, journalctl
- **147-156**: logrotate, GoAccess, promtail, bpftrace, perf, strace/ltrace, gdb, valgrind, Linux capabilities, namespaces
- **157-166**: seccomp, AWS CLI, Azure CLI, GCP CLI, K8s operators, serverless, K3s, MicroK8s, OpenShift CLI
- **167-176**: CPU/topology, memory/hugepages, GPU/CUDA, IPMI/BMC, systemd unit/timers/journal/portable/networkd/resolved/boot
- **177-186**: Btrfs, XFS, ZFS, LVM, mdadm RAID, disk partitioning, LUKS, TPM2, PAM, SSSD
- **187-196**: FreeIPA, Postfix, Dovecot, Apache, Nginx, Caddy, HAProxy, Squid, Varnish, Memcached
- **197-206**: BIND9, Unbound, PowerDNS, OpenStack, OpenDaylight, Open vSwitch, conntrack, tc, OpenVPN, StrongSwan
- **207-216**: Tailscale, Netbird/ZeroTier, FRR/BGP, DHCP, NTP, FTP/SFTP, iSCSI, Ceph, GlusterFS, Restic/Borg
- **217-226**: Duplicity, rclone, rsync, Flatpak/Snap, Nix, AppImage, Gentoo/Portage, Arch/Pacman, Alpine/apk, rpm-ostree
- **227-236**: Buildah, Skopeo, Kaniko, Tekton, ArgoCD, Argo Workflows, FluxCD, Crossplane, Vault, Consul
- **237-246**: Nomad, Boundary, Waypoint, Packer, Spring Boot, GraalVM, Flutter/Dart, React Native, Swift, Kotlin
- **247-256**: Haskell, OCaml, Erlang/Elixir, Lua, R, Julia, Octave, SageMath, Gnuplot, Graphviz
- **257-266**: D2/Mermaid, PlantUML, Pandoc, wkhtmltopdf, LibreOffice, LaTeX, Sphinx, MkDocs, Hugo, Jekyll
- **267-276**: Taskwarrior, Timewarrior, Org-mode, Vim/Neovim, Helix, Micro/Nano, GPG, OpenSSL, hashing, Certbot
- **277-280**: acme.sh/lego, password generation, UUID tools, certificates/TLS

## Format Example

```json
{"instruction": "List all running services", "output": "systemctl list-units --type=service --state=running"}
```

## Getting Started

```bash
# Quick stats
python3 -c "
import json, glob
files = glob.glob('terminal-training-set-nothinking/**/*.json', recursive=True)
total = sum(len(json.load(open(f))) for f in files)
print(f'Total: {total} entries across {len(files)} files')
"
```

## Use Cases

- Fine-tuning language models for Linux/DevOps assistant capabilities
- Training thinking models that reason before acting (chain-of-thought)
- Training non-thinking models for direct command output
- Benchmarking model performance on structured infrastructure tasks

---

## Hybrid Agent Architecture: Using the Worker Model

These datasets train the **`worker`** model (0.5B SLM) that runs locally via Ollama at `http://localhost:11434`. After fine-tuning on `terminal-training-set-nothinking/`, the model outputs bare commands only — no chatter, no markdown.

Pair it with a cloud LLM (Gemini, Claude, GPT) in a **hybrid agent** to save 70–85% on API costs:

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

### Token Cost Comparison

| Workflow Step | Full Cloud Execution | Hybrid Architecture |
| :--- | :--- | :--- |
| **High-level Task Decomposition** | Cloud Tokens | Cloud Tokens |
| **Drafting Terminal Commands** | Cloud Tokens ($$$) | **0 Tokens (Local SLM)** |
| **Command Retries / Syntax Tweaks** | Cloud Tokens ($$$) | **0 Tokens (Local SLM)** |
| **Output Parsing / Verification** | Cloud Tokens | Cloud Tokens |
| **Average Monthly Cost Savings** | **0% Baseline** | **70–85% Saved** |

### Quick Integration

#### Environment Variables

```bash
export OPENAI_API_BASE="http://localhost:11434/v1"
export OPENAI_API_KEY="ollama"
export WORKER_MODEL="worker"
```

#### Python (OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

response = client.chat.completions.create(
    model="worker",
    messages=[
        {"role": "system", "content": "You are a strict, zero-fluff Linux terminal worker."},
        {"role": "user", "content": "List all running services on this Debian server"}
    ],
    temperature=0.0
)

print(response.choices[0].message.content.strip())
# Output: systemctl list-units --type=service --state=running
```

#### Example `opencode.json` Configuration

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

#### Aider CLI

```bash
aider --openai-api-base http://localhost:11434/v1 --openai-api-key ollama --model openai/worker
```

### Best Practices

1. **Keep Temperature at 0.0** — ensures deterministic command generation.
2. **Dry-Run Validation** — always inspect the command before passing to `subprocess.run()`.
3. **Combine Strengths** — use cloud models for planning/debugging, worker for syntax (`find`, `awk`, `grep`, `tar`, `systemctl`).

---

## Licensing

**Proprietary** — Copyright © 2026 Cluster Family / Mohammad Zaid.
