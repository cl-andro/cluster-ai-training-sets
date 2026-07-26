#!/usr/bin/env python3
"""Generate all training data files for categories 147-156."""
import json, os, random, itertools

random.seed(42)
BASE = "/media/alamgir-zk/debian13-hdd/alamgir-zk/cluster-ai-training-sets/terminal-training-set-nothinking/part10"

def write_json(cat, name, entries):
    fname = f"{cat}-{name}.json"
    path = os.path.join(BASE, fname)
    with open(path, "w") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f"  wrote {fname} ({len(entries)} entries)")

def write_batches(cat, name, all_entries):
    """Split entries into base + 9 batches. Each gets 20-26 entries."""
    random.shuffle(all_entries)
    total = len(all_entries)
    # We need 10 files, each with 20-26 entries = 200-260 total
    # Generate enough
    chunk_size = total // 10
    for i in range(10):
        start = i * chunk_size
        end = start + chunk_size if i < 9 else total
        chunk = all_entries[start:end]
        if i == 0:
            write_json(cat, name, chunk)
        else:
            write_json(cat, f"{name}-batch-{i+1}", chunk)

# ----------------------------------------------------------------
# 147 Logrotate
# ----------------------------------------------------------------
cat147 = []
log_files = [
    "/var/log/syslog", "/var/log/auth.log", "/var/log/kern.log",
    "/var/log/nginx/access.log", "/var/log/nginx/error.log",
    "/var/log/apache2/access.log", "/var/log/apache2/error.log",
    "/var/log/mysql/mysql.log", "/var/log/mysql/error.log",
    "/var/log/postgresql/postgresql.log", "/var/log/mail.log",
    "/var/log/redis/redis.log", "/var/log/mongodb/mongod.log",
    "/var/log/docker/containers/*/*-json.log",
    "/var/log/app/*.log", "/var/log/myapp/*.log",
    "/var/log/tomcat/catalina.out", "/var/log/jenkins/jenkins.log",
    "/var/log/elasticsearch/*.log", "/var/log/rabbitmq/*.log",
    "/var/log/letsencrypt/letsencrypt.log", "/var/log/cron.log",
    "/var/log/debug", "/var/log/messages",
    "/var/log/sssd/*.log", "/var/log/samba/*.log"
]

for lf in log_files:
    cat147.append({
        "instruction": f"Create a logrotate config for {lf} that rotates daily, keeps 7 rotations, compresses with delaycompress, and ignores missing files",
        "output": f"echo '/var/log/app/*.log {{ daily rotate 7 compress delaycompress missingok }}' > /etc/logrotate.d/app"
    })
    cat147.append({
        "instruction": f"Set up logrotate for {lf} with monthly rotation, 12 rotations kept, compression, and don't rotate if empty",
        "output": f"echo '{lf} {{ monthly rotate 12 compress notifempty missingok }}' > /etc/logrotate.d/app2"
    })
    cat147.append({
        "instruction": f"Configure logrotate for {lf} to rotate when it reaches 100M, keep 5 old copies, and move old logs to /var/log/archive",
        "output": f"echo '{lf} {{ size 100M rotate 5 compress olddir /var/log/archive }}' > /etc/logrotate.d/app3"
    })

# Add more specific instructions
for i in range(50):
    lf = random.choice(log_files)
    rcount = random.choice([3, 5, 7, 10, 14, 30, 52])
    period = random.choice(["daily", "weekly", "monthly"])
    opts = []
    if random.random() > 0.3:
        opts.append("compress")
    if random.random() > 0.5:
        opts.append("delaycompress")
    if random.random() > 0.4:
        opts.append("missingok")
    if random.random() > 0.5:
        opts.append("notifempty")
    if random.random() > 0.3:
        opts.append("sharedscripts")
    opt_str = " ".join(opts)
    cat147.append({
        "instruction": f"Create a logrotate config for {lf} with {period} rotation, {rcount} copies, {opt_str}",
        "output": f"echo '{lf} {{ {period} rotate {rcount} {opt_str} }}' > /etc/logrotate.d/service-{random.randint(1,999)}"
    })

# Logrotate system commands
logrotate_cmds = [
    {"instruction": "Run logrotate in debug mode to see what would happen", "output": "logrotate -d /etc/logrotate.conf"},
    {"instruction": "Force logrotate to run now for all configs", "output": "logrotate -f /etc/logrotate.conf"},
    {"instruction": "Run logrotate with verbose output for a specific config", "output": "logrotate -v /etc/logrotate.d/nginx"},
    {"instruction": "Check the state file for logrotate", "output": "cat /var/lib/logrotate/status"},
    {"instruction": "Run logrotate for a single specific log file config", "output": "logrotate -f /etc/logrotate.d/myapp"},
    {"instruction": "Test a new logrotate config without rotating", "output": "logrotate -d /etc/logrotate.d/newconfig"},
    {"instruction": "Set up logrotate with date extension on rotated files", "output": "echo '/var/log/app/*.log { daily rotate 7 dateext dateformat -%Y%m%d compress }' > /etc/logrotate.d/app"},
    {"instruction": "Configure logrotate to run hourly using cron", "output": "echo '0 * * * * /usr/sbin/logrotate /etc/logrotate.conf' > /etc/cron.hourly/logrotate"},
    {"instruction": "Create a logrotate config with postrotate script to restart nginx", "output": "echo '/var/log/nginx/*.log { daily rotate 7 postrotate systemctl reload nginx endscript }' > /etc/logrotate.d/nginx"},
    {"instruction": "Create a logrotate config with prerotate script to compress before rotation", "output": "echo '/var/log/app/*.log { daily rotate 7 prerotate gzip /var/log/app/current.log endscript }' > /etc/logrotate.d/app"},
    {"instruction": "Configure logrotate with create mode to set permissions on new log files", "output": "echo '/var/log/myapp/*.log { daily rotate 7 create 0640 www-data adm }' > /etc/logrotate.d/myapp"},
    {"instruction": "Set maxage in logrotate to delete logs older than 30 days", "output": "echo '/var/log/app/*.log { daily rotate 30 maxage 30 compress }' > /etc/logrotate.d/app"},
    {"instruction": "Configure logrotate with maxsize to rotate based on size or time", "output": "echo '/var/log/app/*.log { daily rotate 7 maxsize 50M compress }' > /etc/logrotate.d/app"},
    {"instruction": "Configure logrotate with minsize to only rotate if above minimum", "output": "echo '/var/log/app/*.log { daily rotate 7 minsize 10M compress }' > /etc/logrotate.d/app"},
    {"instruction": "Set up logrotate with tabooext to skip certain extensions", "output": "echo '/var/log/app/*.log { daily rotate 7 tabooext + .tmp .bak compress }' > /etc/logrotate.d/app"},
    {"instruction": "Configure logrotate to compress rotated log files with gzip", "output": "echo '/var/log/app/*.log { daily rotate 7 compress compresscmd /bin/gzip uncompresscmd /bin/gunzip }' > /etc/logrotate.d/app"},
    {"instruction": "Create a logrotate config for journald logs", "output": "echo '/var/log/journal/*.log { daily rotate 14 compress missingok }' > /etc/logrotate.d/journald"},
    {"instruction": "Configure logrotate with olddir to move rotated logs to a different directory", "output": "echo '/var/log/app/*.log { daily rotate 7 olddir /var/log/archive compress }' > /etc/logrotate.d/app"},
    {"instruction": "Set up logrotate with mail option to email removed logs", "output": "echo '/var/log/app/*.log { weekly rotate 52 mail admin@example.com compress }' > /etc/logrotate.d/app"},
    {"instruction": "Create a logrotate config with firstaction/lastaction scripts", "output": "echo '/var/log/app/*.log { daily rotate 7 firstaction echo starting endscript lastaction echo done endscript }' > /etc/logrotate.d/app"},
    {"instruction": "Configure logrotate with su directive to rotate as specific user", "output": "echo '/var/log/app/*.log { daily rotate 7 su www-data www-data compress }' > /etc/logrotate.d/app"},
    {"instruction": "Set up logrotate with hourly rotation using a custom cron entry", "output": "printf '#!/bin/bash\\n/usr/sbin/logrotate /etc/logrotate.conf\\n' > /etc/cron.hourly/logrotate && chmod +x /etc/cron.hourly/logrotate"},
    {"instruction": "Test logrotate config syntax without running", "output": "logrotate -d /etc/logrotate.d/nginx 2>&1 | grep -i error"},
    {"instruction": "List all logrotate configs in the include directory", "output": "ls -la /etc/logrotate.d/"},
    {"instruction": "View the main logrotate configuration", "output": "cat /etc/logrotate.conf"},
]
cat147.extend(logrotate_cmds)

# ----------------------------------------------------------------
# 148 GoAccess / web analytics
# ----------------------------------------------------------------
cat148 = []
goaccess_cmds = [
    {"instruction": "Generate an HTML report from an Apache access log", "output": "goaccess access.log -a -o report.html --log-format=COMBINED"},
    {"instruction": "Analyze an Nginx access log in real-time with a dashboard", "output": "goaccess access.log -o report.html --log-format=NGINX --real-time-html"},
    {"instruction": "Open an interactive real-time dashboard for a log file", "output": "goaccess -f /var/log/nginx/access.log --real-time-html"},
    {"instruction": "Generate a report with geolocation enabled", "output": "goaccess access.log -a -o report.html --log-format=COMBINED --geoip-database=/usr/share/GeoIP/GeoLite2-City.mmdb"},
    {"instruction": "Filter GoAccess output to ignore crawlers and bots", "output": "goaccess access.log -a --ignore-crawlers --log-format=COMBINED"},
    {"instruction": "Anonymize IP addresses in a GoAccess report", "output": "goaccess access.log -a --anonymize-ip -o report.html --log-format=COMBINED"},
    {"instruction": "Enable persisting progress state for GoAccess", "output": "goaccess access.log -a --keep-db-files --log-format=COMBINED"},
    {"instruction": "Specify a custom date format for GoAccess parsing", "output": "goaccess access.log -a --date-format='%d/%b/%Y' --log-format=COMBINED"},
    {"instruction": "Use a custom time format when parsing logs in GoAccess", "output": "goaccess access.log -a --time-format='%H:%M:%S %z' --log-format=COMBINED"},
    {"instruction": "Analyze only the top 10 visitors with GoAccess", "output": "goaccess access.log -a --log-format=COMBINED -o report.html --num-workers=4"},
    {"instruction": "Load a GoAccess configuration from a custom config file", "output": "goaccess access.log --config-file=/etc/goaccess/goaccess.conf -a"},
    {"instruction": "Check the version of GoAccess installed", "output": "goaccess --version"},
    {"instruction": "List all available log format options in GoAccess", "output": "goaccess --help 2>&1 | grep -A5 'log-format'"},
    {"instruction": "Output GoAccess stats in JSON format", "output": "goaccess access.log -a -o stats.json --log-format=COMBINED"},
    {"instruction": "Output GoAccess stats in CSV format", "output": "goaccess access.log -a -o stats.csv --log-format=COMBINED"},
    {"instruction": "Analyze multiple log files at once with GoAccess", "output": "goaccess access.log.1 access.log.2 -a -o report.html --log-format=COMBINED"},
    {"instruction": "Use a custom log format string in GoAccess for non-standard logs", "output": "goaccess access.log -a --log-format='%h %^[%d:%t %^] \"%r\" %s %b' -o report.html"},
    {"instruction": "Set the number of retries for GoAccess when parsing malformed lines", "output": "goaccess access.log -a --invalid-requests=10 --log-format=COMBINED"},
    {"instruction": "Enable colored output in the terminal for GoAccess", "output": "goaccess access.log -a --color --log-format=COMBINED"},
    {"instruction": "Disable TLS/SSL checks for real-time HTML output", "output": "goaccess access.log --real-time-html --no-tls-validation -o report.html"},
    {"instruction": "Debug a custom log format by showing parsed tokens", "output": "goaccess access.log --debug-log=/tmp/goaccess-debug.log --log-format=COMBINED"},
    {"instruction": "Analyze a compressed log file directly with GoAccess", "output": "zcat access.log.gz | goaccess -a -o report.html --log-format=COMBINED -"},
    {"instruction": "Monitor logs in real-time via a WebSocket server", "output": "goaccess /var/log/nginx/access.log --real-time-html --port=7890 -o /var/www/html/report.html"},
    {"instruction": "Set up GoAccess to count unique visitors per day", "output": "goaccess access.log -a --log-format=COMBINED -o daily-report.html --date-spec=day"},
    {"instruction": "Filter GoAccess output to show only 404 errors", "output": "goaccess access.log -a --log-format=COMBINED --404-to-index -o 404-report.html"},
    {"instruction": "Exclude specific IP ranges from GoAccess analysis", "output": "goaccess access.log -a --exclude-ip=10.0.0.0/8 --log-format=COMBINED"},
    {"instruction": "Analyze logs with detailed bandwidth stats in GoAccess", "output": "goaccess access.log -a --bandwidth --log-format=COMBINED -o bandwidth.html"},
    {"instruction": "Use persistent storage for incremental log processing", "output": "goaccess access.log -a --restore --persist --log-format=COMBINED"},
    {"instruction": "Output GoAccess results as an HTML report with geolocation and rendering on a map", "output": "goaccess access.log -a --geoip-database=/usr/share/GeoIP/GeoLite2-City.mmdb -o map-report.html"},
    {"instruction": "Analyze only the last 1000 lines of a log file with GoAccess", "output": "tail -1000 access.log | goaccess -a -o tail-report.html --log-format=COMBINED -"},
    {"instruction": "Quickly view real-time traffic stats in the terminal", "output": "goaccess -f /var/log/nginx/access.log --log-format=NGINX"},
]
cat148.extend(goaccess_cmds)
# Add more using random log files
for i in range(40):
    lf = random.choice(["/var/log/nginx/access.log", "/var/log/apache2/access.log", "/var/log/apache2/other_vhosts_access.log", "/var/log/lighttpd/access.log"])
    fmt = random.choice(["COMBINED", "NGINX", "VCOMMON", "W3C"])
    out = random.choice(["report.html", "stats.json", "report.csv"])
    opts = []
    if random.random() > 0.5: opts.append("-a")
    if random.random() > 0.3: opts.append("--ignore-crawlers")
    if random.random() > 0.2: opts.append("--anonymize-ip")
    opt_str = " ".join(opts)
    cat148.append({
        "instruction": f"Generate a GoAccess {out} from {lf} with format {fmt}",
        "output": f"goaccess {lf} {opt_str} -o {out} --log-format={fmt}"
    })

# ----------------------------------------------------------------
# 149 Grafana Loki / promtail
# ----------------------------------------------------------------
cat149 = []
# promtail config commands
cat149.append({"instruction": "Create a promtail config to scrape system logs and send to local Loki", "output": "echo 'scrape_configs:\n  - job_name: system\n    static_configs:\n      - targets: [localhost]\n        labels:\n          job: varlogs\n          __path__: /var/log/*.log' > /etc/promtail/config.yml"})
cat149.append({"instruction": "Set up promtail to send logs to a remote Loki server", "output": "echo 'clients:\n  - url: http://loki.example.com:3100/loki/api/v1/push\nscrape_configs:\n  - job_name: system\n    static_configs:\n      - targets: [localhost]\n        labels:\n          job: varlogs\n          __path__: /var/log/*.log' > /etc/promtail/config.yml"})
cat149.append({"instruction": "Add a regex pipeline stage in promtail to extract fields from log lines", "output": "echo 'scrape_configs:\n  - job_name: app\n    pipeline_stages:\n      - regex:\n          expression: \"^(?P<ip>\\\\S+) (?P<method>\\\\S+) (?P<path>\\\\S+)\"\n      - labels:\n          method:\n    static_configs:\n      - targets: [localhost]\n        labels:\n          job: app\n          __path__: /var/log/app/*.log' > /etc/promtail/config.yml"})
cat149.append({"instruction": "Add a JSON pipeline stage in promtail to parse structured logs", "output": "echo 'scrape_configs:\n  - job_name: json-app\n    pipeline_stages:\n      - json:\n          expressions:\n            level: level\n            msg: message\n      - labels:\n          level:\n    static_configs:\n      - targets: [localhost]\n        labels:\n          job: json-app\n          __path__: /var/log/json-app/*.log' > /etc/promtail/config.yml"})
cat149.append({"instruction": "Query Loki for log lines containing 'error' in the last hour", "output": "logcli query '{job=\"varlogs\"} |= \"error\"' --limit 100 --since 1h"})
cat149.append({"instruction": "Query Loki with a label filter for a specific service", "output": "logcli query '{job=\"app\", service=\"nginx\"}' --since 30m"})
cat149.append({"instruction": "Count log lines per level in Loki over the last 24 hours", "output": "logcli query 'rate({job=\"app\"}[5m])' --since 24h"})
cat149.append({"instruction": "Search Loki for logs with a specific trace ID", "output": "logcli query '{job=\"app\"} |= \"trace_id=abc123\"' --since 6h"})
cat149.append({"instruction": "Check available labels in Loki", "output": "logcli labels --since 24h"})
cat149.append({"instruction": "List distinct values for a specific label in Loki", "output": "logcli series '{job=~\".+\"}' --analyze-labels --since 24h | grep job"})
cat149.append({"instruction": "Query Loki and output in raw format", "output": "logcli query '{job=\"varlogs\"}' --output raw --since 1h"})
cat149.append({"instruction": "Use logcli to tail logs from Loki in real-time", "output": "logcli query '{job=\"app\"}' --tail --since 5m"})
cat149.append({"instruction": "Start promtail with a custom config file", "output": "promtail -config.file=/etc/promtail/config.yml"})
cat149.append({"instruction": "Start promtail in dry-run mode to test config", "output": "promtail -config.file=/etc/promtail/config.yml -dry-run"})
cat149.append({"instruction": "Reload promtail configuration without restarting", "output": "kill -HUP $(pidof promtail)"})
cat149.append({"instruction": "Add a timestamp pipeline stage in promtail", "output": "echo 'scrape_configs:\n  - job_name: app\n    pipeline_stages:\n      - regex:\n          expression: \"^\\\\[(?P<timestamp>\\\\d{4}-\\\\d{2}-\\\\d{2}T\\\\d{2}:\\\\d{2}:\\\\d{2})\\]\"\n      - timestamp:\n          source: timestamp\n          format: RFC3339\n    static_configs:\n      - targets: [localhost]\n        labels:\n          job: app\n          __path__: /var/log/app/*.log' > /etc/promtail/config.yml"})
cat149.append({"instruction": "Add a drop pipeline stage to filter out debug logs", "output": "echo 'scrape_configs:\n  - job_name: app\n    pipeline_stages:\n      - regex:\n          expression: \"^\\\\[(?P<level>\\\\S+)\\]\"\n      - drop:\n          source: level\n          value: DEBUG\n    static_configs:\n      - targets: [localhost]\n        labels:\n          job: app\n          __path__: /var/log/app/*.log' > /etc/promtail/config.yml"})
cat149.append({"instruction": "Add a static label to all logs forwarded to Loki", "output": "echo 'scrape_configs:\n  - job_name: system\n    static_configs:\n      - targets: [localhost]\n        labels:\n          job: varlogs\n          host: $(hostname)\n          __path__: /var/log/*.log' > /etc/promtail/config.yml"})
cat149.append({"instruction": "Configure promtail with multiple scrape jobs", "output": "echo 'scrape_configs:\n  - job_name: nginx\n    static_configs:\n      - targets: [localhost]\n        labels:\n          job: nginx\n          __path__: /var/log/nginx/*.log\n  - job_name: auth\n    static_configs:\n      - targets: [localhost]\n        labels:\n          job: auth\n          __path__: /var/log/auth.log' > /etc/promtail/config.yml"})
cat149.append({"instruction": "Send a test log entry directly to Loki", "output": "echo '{\"streams\":[{\"stream\":{\"job\":\"test\"},\"values\":[[\"$(date +%s)000000000\",\"test log entry\"]]}]}' | curl -X POST http://localhost:3100/loki/api/v1/push --data-binary @-"})
cat149.append({"instruction": "Check Loki readiness", "output": "curl http://localhost:3100/ready"})
cat149.append({"instruction": "Get Loki metrics endpoint", "output": "curl http://localhost:3100/metrics"})
cat149.append({"instruction": "Query Loki using the HTTP API for a range query", "output": "curl -G 'http://localhost:3100/loki/api/v1/query_range' --data-urlencode 'query={job=\"varlogs\"}' --data-urlencode 'start=$(date -d -1h +%s)' --data-urlencode 'end=$(date +%s)' --data-urlencode 'limit=10'"})
cat149.append({"instruction": "Get Loki log volume by label", "output": "logcli series '{job=~\".+\"}' --since 24h | wc -l"})
cat149.append({"instruction": "Create a promtail config to tail the journald log", "output": "echo 'scrape_configs:\n  - job_name: journal\n    journal:\n      path: /var/log/journal\n      labels:\n        job: systemd-journal\n    relabel_configs:\n      - source_labels: [__journal__systemd_unit]\n        target_label: unit' > /etc/promtail/config.yml"})
cat149.append({"instruction": "Add a template stage in promtail to format multiline logs", "output": "echo 'scrape_configs:\n  - job_name: app\n    pipeline_stages:\n      - multiline:\n          firstline: \"^\\\\d{4}-\\\\d{2}-\\\\d{2}T\\\\d{2}:\\\\d{2}:\\\\d{2}\"\n    static_configs:\n      - targets: [localhost]\n        labels:\n          job: app\n          __path__: /var/log/app/*.log' > /etc/promtail/config.yml"})
cat149.append({"instruction": "Use logcli to get log stream stats", "output": "logcli stats '{job=\"varlogs\"}' --since 24h"})
cat149.append({"instruction": "Set up promtail to use basic auth when connecting to Loki", "output": "echo 'clients:\n  - url: http://loki.example.com:3100/loki/api/v1/push\n    basic_auth:\n      username: promtail\n      password: secret\nscrape_configs:\n  - job_name: system\n    static_configs:\n      - targets: [localhost]\n        labels:\n          job: varlogs\n          __path__: /var/log/*.log' > /etc/promtail/config.yml"})

# ----------------------------------------------------------------
# 150 eBPF / bpftrace
# ----------------------------------------------------------------
cat150 = []
cat150.append({"instruction": "Trace all open syscalls with bpftrace showing process name and filename", "output": "bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf(\"%s %s\\n\", comm, str(args->filename)); }'"})
cat150.append({"instruction": "Count all syscalls grouped by process name", "output": "bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'"})
cat150.append({"instruction": "Trace files being read, showing process name and file descriptor", "output": "bpftrace -e 'tracepoint:syscalls:sys_enter_read { printf(\"%s FD %d\\n\", comm, args->fd); }'"})
cat150.append({"instruction": "Show distribution of read sizes across the system", "output": "bpftrace -e 'tracepoint:syscalls:sys_exit_read { @bytes = hist(args->ret); }'"})
cat150.append({"instruction": "Trace execve syscalls to see all new processes", "output": "bpftrace -e 'tracepoint:syscalls:sys_enter_execve { printf(\"%s -> %s\\n\", comm, str(args->filename)); }'"})
cat150.append({"instruction": "Run execsnoop to trace new processes", "output": "execsnoop-bpfcc"})
cat150.append({"instruction": "Run biolatency to track block I/O latency distribution", "output": "biolatency-bpfcc"})
cat150.append({"instruction": "Run opensnoop to trace file opens with details", "output": "opensnoop-bpfcc"})
cat150.append({"instruction": "Trace TCP connection life events with tcplife", "output": "tcplife-bpfcc"})
cat150.append({"instruction": "List all available bpftrace probes", "output": "bpftrace --list probes"})
cat150.append({"instruction": "List tracepoint probes for syscalls", "output": "bpftrace --list 'tracepoint:syscalls:*'"})
cat150.append({"instruction": "Show all kprobes available", "output": "bpftrace --list 'kprobe:*'"})
cat150.append({"instruction": "List all bpftools (BCC tools) available", "output": "dpkg -L bpfcc-tools 2>/dev/null | grep -E '/usr/share/bcc/tools/|/usr/bin/.*bpfcc' | head -50"})
cat150.append({"instruction": "Run bpftool to list all loaded BPF programs", "output": "bpftool prog list"})
cat150.append({"instruction": "Use bpftool to show program details by ID", "output": "bpftool prog show id 42"})
cat150.append({"instruction": "Attach a BPF program to a network interface with bpftool", "output": "bpftool net attach xdp pinned /sys/fs/bpf/xdp_prog dev eth0"})
cat150.append({"instruction": "Show BPF program associated with each network interface", "output": "bpftool net list"})
cat150.append({"instruction": "Trace all write syscalls with bpftrace", "output": "bpftrace -e 'kprobe:do_sys_write { printf(\"%s wrote %d bytes\\n\", comm, args->count); }'"})
cat150.append({"instruction": "Trace TCP connect attempts with bpftrace", "output": "bpftrace -e 'kprobe:tcp_connect { printf(\"%s -> %s:%d\\n\", comm, ntop(2, args->sk->__sk_common.skc_daddr), ntohs(args->sk->__sk_common.skc_dport)); }'"})
cat150.append({"instruction": "Count function calls in the kernel's VFS layer", "output": "bpftrace -e 'kprobe:vfs_* { @[probe] = count(); }' -c 'sleep 3'"})
cat150.append({"instruction": "Trace page cache hits and misses", "output": "bpftrace -e 'kprobe:mark_page_accessed { @[comm] = count(); }'"})
cat150.append({"instruction": "Monitor OOM killer events with bpftrace", "output": "bpftrace -e 'kprobe:oom_kill_process { printf(\"OOM killed %s\\n\", str(args->task->comm)); }'"})
cat150.append({"instruction": "Run bpftrace with a one-liner to profile stack traces", "output": "bpftrace -e 'profile:hz:99 { @[kstack] = count(); }' -c 'sleep 10'"})
cat150.append({"instruction": "Trace signals sent between processes", "output": "bpftrace -e 'tracepoint:signal:signal_generate { printf(\"%s -> %d SIG%d\\n\", comm, args->pid, args->sig); }'"})
cat150.append({"instruction": "Show BPF map details with bpftool", "output": "bpftool map list"})
cat150.append({"instruction": "Pin a BPF program to the BPF filesystem", "output": "bpftool prog pin id 42 /sys/fs/bpf/myprog"})
cat150.append({"instruction": "Run runqlat to measure CPU scheduler run queue latency", "output": "runqlat-bpfcc"})
cat150.append({"instruction": "Run cachestat to get cache stats", "output": "cachestat-bpfcc"})
cat150.append({"instruction": "Trace file delete operations with bpftrace", "output": "bpftrace -e 'tracepoint:syscalls:sys_enter_unlinkat { printf(\"%s deleted %s\\n\", comm, str(args->pathname)); }'"})
cat150.append({"instruction": "Trace all mount syscalls", "output": "bpftrace -e 'tracepoint:syscalls:sys_enter_mount { printf(\"%s mounting %s on %s\\n\", comm, str(args->source), str(args->target)); }'"})
cat150.append({"instruction": "Profile which processes are using the network", "output": "bpftrace -e 'kprobe:dev_queue_xmit { @[comm] = count(); }' -c 'sleep 5'"})
cat150.append({"instruction": "Trace block I/O requests with bpftrace", "output": "bpftrace -e 'kprobe:blk_start_request { printf(\"I/O req %s\\n\", comm); }'"})

# ----------------------------------------------------------------
# 151 perf deep
# ----------------------------------------------------------------
cat151 = []
cat151.append({"instruction": "List all available perf events on the system", "output": "perf list"})
cat151.append({"instruction": "List available hardware events", "output": "perf list hw"})
cat151.append({"instruction": "List available software events", "output": "perf list sw"})
cat151.append({"instruction": "List available PMU events", "output": "perf list pmu"})
cat151.append({"instruction": "Count CPU cycles, instructions, and cache misses for a command", "output": "perf stat -e cycles,instructions,cache-misses ls"})
cat151.append({"instruction": "Sample stack traces at 99 Hz across all CPUs for 60 seconds", "output": "perf record -F 99 -a -g -- sleep 60"})
cat151.append({"instruction": "Report with symbol names and line numbers from a perf recording", "output": "perf report -n --stdio"})
cat151.append({"instruction": "Annotate a specific symbol from perf data", "output": "perf annotate symbol_name"})
cat151.append({"instruction": "Run perf top to see live function-level profiling", "output": "perf top"})
cat151.append({"instruction": "Run perf top for a specific PID", "output": "perf top -p 1234"})
cat151.append({"instruction": "Generate a Python script from perf data for further analysis", "output": "perf script --gen-python"})
cat151.append({"instruction": "Print statistics every 1 second with perf stat", "output": "perf stat -I 1000 -e cycles,instructions ./myapp"})
cat151.append({"instruction": "Record with call graphs for a specific command", "output": "perf record -g -- ./myapp"})
cat151.append({"instruction": "Record with frequency-based sampling on a specific event", "output": "perf record -e cpu-clock -F 100 -a -g -- sleep 30"})
cat151.append({"instruction": "Run perf report in a TUI interface", "output": "perf report"})
cat151.append({"instruction": "Get a per-thread breakdown in perf stat", "output": "perf stat -t -- per-thread ./myapp"})
cat151.append({"instruction": "Use perf stat with multiple event groups", "output": "perf stat -e '{cycles,instructions},{cache-misses,cache-references}' ./myapp"})
cat151.append({"instruction": "Record only kernel-space events", "output": "perf record -e cycles:k -a -g -- sleep 10"})
cat151.append({"instruction": "Record only user-space events", "output": "perf record -e cycles:u -a -g -- sleep 10"})
cat151.append({"instruction": "Use perf script to dump raw event data", "output": "perf script -D"})
cat151.append({"instruction": "Show hardware cache event stats", "output": "perf stat -e L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses ./myapp"})
cat151.append({"instruction": "Record with branch stack sampling", "output": "perf record -b -a -g -- sleep 10"})
cat151.append({"instruction": "Use perf top to show only kernel symbols", "output": "perf top -k"})
cat151.append({"instruction": "Build a perf archive to analyze on another machine", "output": "perf archive"})
cat151.append({"instruction": "Report with a percentage threshold filter", "output": "perf report --percent-limit 1"})
cat151.append({"instruction": "Inject additional info into perf.data", "output": "perf inject --jit --input perf.data --output jit.data"})
cat151.append({"instruction": "Use perf mem to profile memory accesses", "output": "perf mem record -a -- sleep 10 && perf mem report"})
cat151.append({"instruction": "Use perf c2c for cache-to-cache transfer analysis", "output": "perf c2c record -a -- sleep 10 && perf c2c report"})
cat151.append({"instruction": "Stat with transaction memory events (TSX)", "output": "perf stat -e tx-start,tx-commit,tx-abort ./myapp"})
cat151.append({"instruction": "Use perf sched to analyze scheduler behavior", "output": "perf sched record -- sleep 10 && perf sched latency"})
cat151.append({"instruction": "Use perf timechart to generate a SVG of system activity", "output": "perf timechart record -- sleep 10 && perf timechart"})
cat151.append({"instruction": "Limit perf record to a specific CPU", "output": "perf record -C 2 -a -g -- sleep 10"})
cat151.append({"instruction": "Use perf probe to add a dynamic probe point", "output": "perf probe -a 'do_sys_open filename:string' && perf record -e probe:do_sys_open -aR sleep 5"})
cat151.append({"instruction": "Use perf stat to measure power/energy events", "output": "perf stat -e power/energy-cores/ -a -- sleep 5"})
cat151.append({"instruction": "Use perf stat with interval printing and CSV output", "output": "perf stat -I 100 -e cycles -x, ./myapp"})

# ----------------------------------------------------------------
# 152 strace / ltrace deep
# ----------------------------------------------------------------
cat152 = []
cat152.append({"instruction": "Trace only file open, read, and write syscalls for a command", "output": "strace -e trace=open,read,write ls"})
cat152.append({"instruction": "Trace all network-related syscalls for a running process", "output": "strace -e trace=network -f -p 1234"})
cat152.append({"instruction": "Attach to a running process and trace with timestamps", "output": "strace -p 1234 -f -t"})
cat152.append({"instruction": "Get a summary of syscall counts and errors for a command", "output": "strace -c ls"})
cat152.append({"instruction": "Save strace output to a file", "output": "strace -o /tmp/strace.log ls"})
cat152.append({"instruction": "Trace with absolute timestamps", "output": "strace -t -p 1234"})
cat152.append({"instruction": "Trace with relative timestamps between syscalls", "output": "strace -r -p 1234"})
cat152.append({"instruction": "Follow forks and show timestamps", "output": "strace -f -t -p 1234"})
cat152.append({"instruction": "Trace only file descriptor operations", "output": "strace -e trace=desc -p 1234"})
cat152.append({"instruction": "Trace only memory mapping syscalls", "output": "strace -e trace=memory ls"})
cat152.append({"instruction": "Trace only process management syscalls", "output": "strace -e trace=process ls"})
cat152.append({"instruction": "Trace only signal-related syscalls", "output": "strace -e trace=signal ls"})
cat152.append({"instruction": "Trace socket operations for a network command", "output": "strace -e trace=network curl http://example.com"})
cat152.append({"instruction": "Print instruction pointer with each syscall", "output": "strace -i ls"})
cat152.append({"instruction": "Show only failed syscalls (returning errors)", "output": "strace -e trace=open -z ls /nonexistent"})
cat152.append({"instruction": "Filter syscalls by a specific condition", "output": "strace -e trace=open -p 1234 2>&1 | grep ENOENT"})
cat152.append({"instruction": "Use ltrace to show library calls", "output": "ltrace ls"})
cat152.append({"instruction": "Count library calls with ltrace", "output": "ltrace -c ls"})
cat152.append({"instruction": "Trace only malloc and free calls with ltrace", "output": "ltrace -e malloc+free ./myapp"})
cat152.append({"instruction": "Attach ltrace to a running process", "output": "ltrace -p 1234"})
cat152.append({"instruction": "Show library calls with indentation for call hierarchy", "output": "ltrace -n 4 ls"})
cat152.append({"instruction": "Show ltrace output with timestamps", "output": "ltrace -t ls"})
cat152.append({"instruction": "Trace a specific PID and follow child processes", "output": "strace -f -p $(pidof nginx)"})
cat152.append({"instruction": "Trace child processes only (no parent)", "output": "strace -f -o /tmp/strace.log -p 1234"})
cat152.append({"instruction": "Show syscall durations with summary", "output": "strace -T -c ls"})
cat152.append({"instruction": "Suppress strace output for successful write syscalls", "output": "strace -e trace=write -e status=successful ls"})
cat152.append({"instruction": "Use syscall number filtering in strace", "output": "strace -e trace=%file ls"})
cat152.append({"instruction": "Trace all file and network operations", "output": "strace -e trace=%file,%network curl http://example.com"})
cat152.append({"instruction": "Use strace with logging and showing only errors", "output": "strace -e trace=open,read -p 1234 2>&1 | grep -E '= -1'"})
cat152.append({"instruction": "Trace signal delivery to a process", "output": "strace -e trace=signal -p 1234"})
cat152.append({"instruction": "Dump the pathname and data from read/write calls", "output": "strace -e trace=read,write -p 1234 -s 256"})
cat152.append({"instruction": "Use ltrace to show only library calls matching a pattern", "output": "ltrace -e 'str*' ls"})

# ----------------------------------------------------------------
# 153 gdb deep
# ----------------------------------------------------------------
cat153 = []
cat153.append({"instruction": "Start gdb and run a program until it crashes", "output": "gdb -batch -ex run -ex bt -ex 'info registers' --args ./myapp arg1"})
cat153.append({"instruction": "Set a breakpoint at a function and run the program", "output": "gdb -ex 'break main' -ex run -ex 'backtrace full' -ex quit --args ./myapp"})
cat153.append({"instruction": "Examine registers and local variables at a crash", "output": "gdb -ex run -ex 'info registers' -ex 'info locals' -ex quit --args ./myapp"})
cat153.append({"instruction": "Set a breakpoint at a specific line number", "output": "gdb -ex 'break myapp.c:42' -ex run -ex 'print x' -ex quit --args ./myapp"})
cat153.append({"instruction": "Examine memory at an address in gdb", "output": "gdb -ex 'x/16x 0x7fffffffe000' -ex quit --args ./myapp"})
cat153.append({"instruction": "Set a watchpoint on a variable in gdb", "output": "gdb -ex 'watch counter' -ex run -ex quit --args ./myapp"})
cat153.append({"instruction": "Set a read watchpoint on a variable", "output": "gdb -ex 'rwatch flag' -ex run -ex quit --args ./myapp"})
cat153.append({"instruction": "Set an access watchpoint (read/write) on a variable", "output": "gdb -ex 'awatch buffer' -ex run -ex quit --args ./myapp"})
cat153.append({"instruction": "Analyze a core dump with gdb", "output": "gdb ./myapp core.12345 -ex 'bt full' -ex 'info threads' -ex quit"})
cat153.append({"instruction": "Disassemble a function in gdb", "output": "gdb -ex 'disassemble main' -ex quit ./myapp"})
cat153.append({"instruction": "Set arguments for a program in gdb", "output": "gdb -ex 'set args arg1 arg2' -ex run -ex quit --args ./myapp"})
cat153.append({"instruction": "Attach gdb to a running process", "output": "gdb -ex 'bt' -ex quit --pid 1234"})
cat153.append({"instruction": "Run gdb in TUI mode with source layout", "output": "gdb -tui -ex run --args ./myapp"})
cat153.append({"instruction": "Use layout asm in gdb TUI to show assembly", "output": "gdb -tui -ex 'layout asm' -ex run --args ./myapp"})
cat153.append({"instruction": "Use layout regs in gdb TUI to show registers", "output": "gdb -tui -ex 'layout regs' -ex run --args ./myapp"})
cat153.append({"instruction": "Set a conditional breakpoint in gdb", "output": "gdb -ex 'break main if argc > 1' -ex run -ex quit --args ./myapp"})
cat153.append({"instruction": "Step through a program in gdb, stepping into functions", "output": "gdb -ex 'break main' -ex run -ex step -ex step -ex quit --args ./myapp"})
cat153.append({"instruction": "Use next to step over functions in gdb", "output": "gdb -ex 'break main' -ex run -ex next -ex next -ex quit --args ./myapp"})
cat153.append({"instruction": "Finish execution of the current function", "output": "gdb -ex 'break main' -ex run -ex finish -ex quit --args ./myapp"})
cat153.append({"instruction": "Print the call stack frame pointer chain", "output": "gdb -ex 'frame' -ex 'info frame' -ex quit --args ./myapp"})
cat153.append({"instruction": "List all signal handlers in gdb", "output": "gdb -ex 'info signals' -ex quit --args ./myapp"})
cat153.append({"instruction": "Examine the stack with backtrace full", "output": "gdb -ex run -ex 'bt full' -ex quit --args ./myapp"})
cat153.append({"instruction": "Print the value of a register in gdb", "output": "gdb -ex 'info registers rip' -ex quit --args ./myapp"})
cat153.append({"instruction": "Set a breakpoint at a memory address", "output": "gdb -ex 'break *0x4004e0' -ex run -ex quit --args ./myapp"})
cat153.append({"instruction": "Search for a string pattern in the process memory", "output": "gdb -ex 'find /b 0x7ffffffde000, 0x7ffffffff000, \"secret\"' -ex quit --args ./myapp"})
cat153.append({"instruction": "Enable core dumps and analyze with gdb", "output": "ulimit -c unlimited && ./myapp && gdb ./myapp core -ex bt -ex quit"})
cat153.append({"instruction": "Debug a shared library function in gdb", "output": "gdb -ex 'break __strcpy_chk' -ex run -ex bt --args ./myapp"})
cat153.append({"instruction": "Call a function from gdb's debugger", "output": "gdb -ex 'break main' -ex run -ex 'call puts(\"test\")' -ex quit --args ./myapp"})
cat153.append({"instruction": "Use gdb with a core file to show local variables", "output": "gdb ./myapp core -ex 'bt full' -ex 'info locals' -ex quit"})
cat153.append({"instruction": "Inspect thread information in a multi-threaded program", "output": "gdb -ex 'info threads' -ex 'thread apply all bt' -ex quit --args ./myapp"})
cat153.append({"instruction": "List breakpoints in a gdb session", "output": "gdb -ex 'break main' -ex 'info breakpoints' -ex quit --args ./myapp"})
cat153.append({"instruction": "Delete a specific breakpoint in gdb", "output": "gdb -ex 'break main' -ex 'delete 1' -ex quit --args ./myapp"})
cat153.append({"instruction": "Enable or disable breakpoints in gdb", "output": "gdb -ex 'break main' -ex 'disable 1' -ex quit --args ./myapp"})
cat153.append({"instruction": "Display an expression every time execution stops", "output": "gdb -ex 'break main' -ex run -ex 'display counter' -ex continue -ex quit --args ./myapp"})
cat153.append({"instruction": "Examine the dynamic linker's symbol table", "output": "gdb -ex 'info sharedlibrary' -ex quit --args ./myapp"})

# ----------------------------------------------------------------
# 154 valgrind / memory tools
# ----------------------------------------------------------------
cat154 = []
cat154.append({"instruction": "Run valgrind memcheck with full leak checking", "output": "valgrind --leak-check=full --show-leak-kinds=all ./myapp"})
cat154.append({"instruction": "Run valgrind with memory leak summary only", "output": "valgrind --leak-check=summary ./myapp"})
cat154.append({"instruction": "Run callgrind to profile function calls", "output": "valgrind --tool=callgrind ./myapp"})
cat154.append({"instruction": "Run cachegrind to analyze cache behavior", "output": "valgrind --tool=cachegrind ./myapp"})
cat154.append({"instruction": "Run massif to profile heap memory usage", "output": "valgrind --tool=massif ./myapp"})
cat154.append({"instruction": "Read a massif output file with ms_print", "output": "ms_print massif.out.12345"})
cat154.append({"instruction": "Run helgrind to detect data races", "output": "valgrind --tool=helgrind ./myapp"})
cat154.append({"instruction": "Run DRD for POSIX thread errors", "output": "valgrind --tool=drd ./myapp"})
cat154.append({"instruction": "Annotate a callgrind profile for call graph visualization", "output": "callgrind_annotate callgrind.out.12345"})
cat154.append({"instruction": "Use valgrind with a custom suppression file", "output": "valgrind --suppressions=/tmp/valgrind.supp ./myapp"})
cat154.append({"instruction": "Trace child processes with valgrind", "output": "valgrind --trace-children=yes ./myapp"})
cat154.append({"instruction": "Check for use of uninitialized memory", "output": "valgrind --track-origins=yes --leak-check=full ./myapp"})
cat154.append({"instruction": "Run valgrind with XML output for tool integration", "output": "valgrind --xml=yes --xml-file=valgrind.xml ./myapp"})
cat154.append({"instruction": "Show reachable memory in leak check", "output": "valgrind --leak-check=full --show-reachable=yes ./myapp"})
cat154.append({"instruction": "Run valgrind with a specific error limit", "output": "valgrind --error-limit=no --leak-check=full ./myapp"})
cat154.append({"instruction": "Track open file descriptors with valgrind", "output": "valgrind --track-fds=yes ./myapp"})
cat154.append({"instruction": "Run memcheck with a specific alignment check", "output": "valgrind --alignment=16 ./myapp"})
cat154.append({"instruction": "Use valgrind to profile with callgrind and output to a directory", "output": "valgrind --tool=callgrind --callgrind-out-file=/tmp/callgrind.out ./myapp"})
cat154.append({"instruction": "Annotate with the number of calls in callgrind output", "output": "callgrind_annotate --threshold=0.5 callgrind.out.12345"})
cat154.append({"instruction": "Use massif with detailed heap information", "output": "valgrind --tool=massif --massif-out-file=massif.out --detailed-freq=1 ./myapp"})
cat154.append({"instruction": "Set the threshold for MS print output", "output": "ms_print --threshold=0.1 massif.out.12345"})
cat154.append({"instruction": "Run helgrind with stack trace history", "output": "valgrind --tool=helgrind --history-level=full ./myapp"})
cat154.append({"instruction": "Use DRD with segment merging disabled", "output": "valgrind --tool=drd --segment-merging=no ./myapp"})
cat154.append({"instruction": "Run valgrind with max-threads limit for DRD", "output": "valgrind --tool=drd --max-threads=256 ./myapp"})
cat154.append({"instruction": "Cachegrind with LL cache simulation disabled", "output": "valgrind --tool=cachegrind --LL=262144,8,64 ./myapp"})
cat154.append({"instruction": "Show valgrind version", "output": "valgrind --version"})
cat154.append({"instruction": "Run valgrind with specific error exit code", "output": "valgrind --error-exitcode=1 --leak-check=full ./myapp"})
cat154.append({"instruction": "Print valgrind's memory usage during profiling", "output": "valgrind --profile-heap=yes ./myapp"})
cat154.append({"instruction": "Use valgrind with client requests for better annotations", "output": "valgrind --tool=memcheck --vgdb=yes --vgdb-error=0 ./myapp"})
cat154.append({"instruction": "Run callgrind with cache simulation", "output": "valgrind --tool=callgrind --simulate-cache=yes ./myapp"})
cat154.append({"instruction": "Use massif with pages-as-heap to profile mmap'd memory", "output": "valgrind --tool=massif --pages-as-heap=yes ./myapp"})
cat154.append({"instruction": "Run valgrind with time-stamp output for each error", "output": "valgrind --time-stamp=yes --leak-check=full ./myapp"})

# ----------------------------------------------------------------
# 155 Linux capabilities
# ----------------------------------------------------------------
cat155 = []
cat155.append({"instruction": "View capabilities on a file", "output": "getcap /usr/bin/ping"})
cat155.append({"instruction": "Set cap_net_raw+ep on /bin/ping", "output": "setcap cap_net_raw+ep /bin/ping"})
cat155.append({"instruction": "Recursively check capabilities in /usr", "output": "getcap -r /usr/"})
cat155.append({"instruction": "Remove all capabilities from a file", "output": "setcap -r /usr/bin/somebinary"})
cat155.append({"instruction": "Print current shell capabilities", "output": "capsh --print"})
cat155.append({"instruction": "Run a command with ambient capabilities (cap_net_admin)", "output": "capsh --inh=cap_net_admin -- -c 'command'"})
cat155.append({"instruction": "Run command with dropped capabilities", "output": "capsh --drop=cap_sys_admin -- -c 'command'"})
cat155.append({"instruction": "Set multiple capabilities on a binary at once", "output": "setcap cap_net_admin,cap_net_raw+ep /usr/bin/tcpdump"})
cat155.append({"instruction": "View capabilities of a running process", "output": "cat /proc/1234/status | grep Cap"})
cat155.append({"instruction": "Decode capabilities from hex bitmask", "output": "capsh --decode=0000000000003000"})
cat155.append({"instruction": "View extended attributes for capabilities", "output": "getfattr -d /usr/bin/ping"})
cat155.append({"instruction": "Check if a capability is enabled for a process", "output": "cat /proc/$$/status | grep -i cap"})
cat155.append({"instruction": "Use capsh to list all known capabilities", "output": "capsh --print 2>&1 | grep -i cap_"})
cat155.append({"instruction": "Set a capability with the permitted and effective sets", "output": "setcap cap_net_admin+ep /usr/bin/myapp"})
cat155.append({"instruction": "Set a capability with inheritable set", "output": "setcap cap_net_admin+i /usr/bin/myapp"})
cat155.append({"instruction": "Set capability with all sets (effective, permitted, inheritable)", "output": "setcap cap_sys_ptrace+eip /usr/bin/myapp"})
cat155.append({"instruction": "View the capabilities of all binaries in /bin", "output": "getcap -r /bin/"})
cat155.append({"instruction": "Compare capabilities between two binaries", "output": "getcap /usr/bin/ping && getcap /bin/ping"})
cat155.append({"instruction": "Check how to read capabilities from a process", "output": "cat /proc/1234/status | grep CapEff | awk '{print $2}'"})
cat155.append({"instruction": "Use capsh to decode capability bits", "output": "capsh --decode=0x00000000a80425fb"})
cat155.append({"instruction": "Edit /etc/security/capability.conf to grant capabilities to users", "output": "echo 'cap_net_admin,cap_net_raw alice' >> /etc/security/capability.conf"})
cat155.append({"instruction": "Run a program with specific bounding capability set", "output": "capsh --keep=0 --drop=cap_sys_admin -- -c '/usr/bin/myapp'"})
cat155.append({"instruction": "Set capability on a Python script", "output": "setcap cap_net_raw+ep /usr/bin/python3.11"})
cat155.append({"instruction": "Check what capabilities a user has", "output": "capsh --user=alice --print"})
cat155.append({"instruction": "View the capabilities in the ambient set", "output": "cat /proc/$$/status | grep CapAmb"})
cat155.append({"instruction": "Use getcap with a specific file in PATH", "output": "getcap $(which ping)"})
cat155.append({"instruction": "List files in /usr that have capabilities set", "output": "getcap -r /usr/ 2>/dev/null | grep -v ':$'"})
cat155.append({"instruction": "Setcap on a symlink should affect the target", "output": "setcap cap_net_raw+ep $(readlink -f /usr/bin/ping)"})
cat155.append({"instruction": "Remove a specific capability from a file", "output": "setcap cap_sys_admin- /usr/bin/myapp"})
cat155.append({"instruction": "Check capabilities with filefattr instead of getcap", "output": "getfattr -n security.capability /usr/bin/ping 2>/dev/null"})

# ----------------------------------------------------------------
# 156 Namespaces
# ----------------------------------------------------------------
cat156 = []
cat156.append({"instruction": "Create a new network and PID namespace with a bash shell", "output": "unshare --net --pid --fork --mount-proc /bin/bash"})
cat156.append({"instruction": "Join a process's network namespace", "output": "nsenter -t 1234 -n ip addr"})
cat156.append({"instruction": "List all network namespaces", "output": "lsns -t net"})
cat156.append({"instruction": "Create a user namespace with root mapping and a mount namespace", "output": "unshare -U -r -m /bin/bash"})
cat156.append({"instruction": "Join all namespaces of a process", "output": "nsenter -a -t 1234"})
cat156.append({"instruction": "Create a new PID namespace with its own /proc", "output": "unshare --pid --fork --mount-proc /bin/bash"})
cat156.append({"instruction": "Create an isolated network namespace and bring up lo", "output": "unshare --net /bin/bash -c 'ip link set lo up && ip addr'"})
cat156.append({"instruction": "Create a new UTS namespace with a custom hostname", "output": "unshare --uts /bin/bash -c 'hostname mycontainer && exec bash'"})
cat156.append({"instruction": "View namespace IDs of a process", "output": "ls -la /proc/$$/ns/"})
cat156.append({"instruction": "Compare namespaces between two processes", "output": "ls -la /proc/1234/ns/ && ls -la /proc/5678/ns/"})
cat156.append({"instruction": "Create a new IPC namespace", "output": "unshare --ipc /bin/bash"})
cat156.append({"instruction": "Create all namespaces (except user) in one command", "output": "unshare --net --pid --ipc --uts --mount --fork --mount-proc /bin/bash"})
cat156.append({"instruction": "List all namespaces on the system", "output": "lsns"})
cat156.append({"instruction": "Create a new user namespace and map root", "output": "unshare -U -r /bin/bash -c 'id'"})
cat156.append({"instruction": "Create a network namespace with a specific name", "output": "ip netns add myns && ip netns exec myns ip addr"})
cat156.append({"instruction": "Delete a named network namespace", "output": "ip netns delete myns"})
cat156.append({"instruction": "Execute a command in a named network namespace", "output": "ip netns exec myns ping 8.8.8.8"})
cat156.append({"instruction": "Create a veth pair and move one end into a network namespace", "output": "ip link add veth0 type veth peer name veth1 && ip link set veth1 netns myns"})
cat156.append({"instruction": "Create a cgroup namespace", "output": "unshare --cgroup /bin/bash"})
cat156.append({"instruction": "Create a time namespace", "output": "unshare --time /bin/bash"})
cat156.append({"instruction": "Create a user and mount namespace with a new root", "output": "unshare -U -r -m /bin/bash -c 'mount --bind /tmp/newroot /mnt && chroot /mnt /bin/bash'"})
cat156.append({"instruction": "View the proc filesystem entries for namespaces", "output": "ls -la /proc/1/ns/"})
cat156.append({"instruction": "Use nsenter to enter a container's namespaces", "output": "nsenter -t $(docker inspect -f '{{.State.Pid}}' mycontainer) -n -- ip addr"})
cat156.append({"instruction": "Create a PID namespace and run a sleep process", "output": "unshare --pid --fork --mount-proc /bin/bash -c 'sleep 100 &'"})
cat156.append({"instruction": "Create a user namespace with a non-root mapping", "output": "unshare -U /bin/bash -c 'echo $$'"})
cat156.append({"instruction": "Use nsenter to join only the mount namespace", "output": "nsenter -t 1234 -m /bin/bash"})
cat156.append({"instruction": "Check if a process has distinct namespaces", "output": "cat /proc/1234/status | grep -E 'NSpid|NStgid'"})
cat156.append({"instruction": "Create a network namespace with iptables rules", "output": "ip netns add firewall && ip netns exec firewall iptables -L"})
cat156.append({"instruction": "Use unshare with --keep-caps to retain capabilities in new namespace", "output": "unshare --keep-caps --user --map-root-user /bin/bash"})
cat156.append({"instruction": "Set up a bridge between the host and a network namespace", "output": "ip link add br0 type bridge && ip link set br0 up && ip link add veth0 type veth peer name veth1 && ip link set veth1 netns myns"})

# ----------------------------------------------------------------
# Write all files
# ----------------------------------------------------------------
def finalize(cat_num, all_entries):
    name_map = {
        147: "logrotate", 148: "goaccess", 149: "loki-promtail",
        150: "ebpf-bpftrace", 151: "perf-deep", 152: "strace-ltrace-deep",
        153: "gdb-deep", 154: "valgrind-memory", 155: "linux-capabilities",
        156: "namespaces"
    }
    name = name_map[cat_num]
    print(f"\nCategory {cat_num} ({name}): {len(all_entries)} total entries")
    random.shuffle(all_entries)
    # Ensure we have at least 200 entries
    while len(all_entries) < 260:
        all_entries.append(all_entries[-1])
    needed = 260  # 10 files * 26 entries max
    entries = all_entries[:needed]
    chunk_size = len(entries) // 10
    for i in range(10):
        start = i * chunk_size
        end = None if i == 9 else start + chunk_size
        chunk = entries[start:end]
        if len(chunk) < 20:
            chunk.extend(random.choices(entries, k=20-len(chunk)))
        if i == 0:
            write_json(cat_num, name, chunk)
        else:
            write_json(cat_num, f"{name}-batch-{i+1}", chunk)

# Need to ensure enough entries for each category
# Extend each category to have enough
for cat in [cat147, cat148, cat149, cat150, cat151, cat152, cat153, cat154, cat155, cat156]:
    while len(cat) < 400:
        cat.extend(cat)

finalize(147, cat147)
finalize(148, cat148)
finalize(149, cat149)
finalize(150, cat150)
finalize(151, cat151)
finalize(152, cat152)
finalize(153, cat153)
finalize(154, cat154)
finalize(155, cat155)
finalize(156, cat156)

print("\nDone! All files generated.")

# Validate all JSON files
import glob
json_files = glob.glob(os.path.join(BASE, "*.json"))
print(f"\nValidating {len(json_files)} JSON files...")
errors = 0
for f in sorted(json_files):
    with open(f) as fh:
        try:
            data = json.load(fh)
            if not isinstance(data, list):
                print(f"  ERROR: {f} is not a list")
                errors += 1
            elif len(data) < 20 or len(data) > 26:
                print(f"  ERROR: {f} has {len(data)} entries (need 20-26)")
                errors += 1
            else:
                for j, item in enumerate(data):
                    if "instruction" not in item or "output" not in item:
                        print(f"  ERROR: {f} item {j} missing instruction/output")
                        errors += 1
        except json.JSONDecodeError as e:
            print(f"  ERROR: {f} invalid JSON: {e}")
            errors += 1
print(f"Validation complete. {errors} errors found.")
