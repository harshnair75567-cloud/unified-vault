# Unified Vault

Security monitoring platform combining host-based intrusion prevention (LotL detection, SIGKILL neutralization), network-based intrusion detection (Scapy/socket-based sensors), and file integrity monitoring into a single unified toolkit.

## Modules

| Module | Layer | What it does |
|---|---|---|
| [`ids/`](ids/) | Network | Port-scan + signature-based detection on commonly probed ports |
| [`ips/`](ips/) | Host | Real-time LotL detection with automatic process neutralization |
| [`integrity/`](integrity/) | File | Baseline/audit hash-based tamper detection |

See [docs/architecture.md](docs/architecture.md) for how the layers fit together.

## Usage

```bash
pip install -r requirements.txt

python cli.py --mode ids                          # start network sensor
python cli.py --mode ips                           # start host watcher
python cli.py --mode integrity --baseline /path     # create FIM baseline
python cli.py --mode integrity --audit /path         # audit against baseline
python cli.py --mode all                            # run ids + ips together
```

Config lives in [`config.yaml`](config.yaml).

## Origin

This repo consolidates three previously separate projects — HS-IPS, a Scapy-based NIDS, and PyHash — into one platform with shared logging/config. Original repos are archived.

## License

MIT (see [LICENSE](LICENSE))
