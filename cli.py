"""
Unified Vault CLI
Run host-based IPS, network IDS, and file integrity monitoring
individually or all together, sharing one config and one log stream.

Usage:
    python cli.py --mode ips
    python cli.py --mode ids
    python cli.py --mode integrity --baseline PATH
    python cli.py --mode integrity --audit PATH
    python cli.py --mode integrity --watch PATH [--interval SECONDS]
    python cli.py --mode all                      # runs ids + ips + integrity watch together
"""
import argparse
import subprocess
import sys
import threading
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from core.config_loader import get_config


def run_ips():
    subprocess.run([sys.executable, os.path.join(ROOT, "ips", "TTY-check.py")])


def run_ids():
    subprocess.run([sys.executable, os.path.join(ROOT, "ids", "ids_supporter_v3.py")],
                    cwd=os.path.join(ROOT, "ids"))


def run_integrity(mode, target, interval=None):
    flag = {"baseline": "--baseline", "audit": "--audit", "watch": "--watch"}[mode]
    cmd = [sys.executable, os.path.join(ROOT, "integrity", "pyhashv2", "main.py"), flag, target]
    if mode == "watch" and interval:
        cmd.append(str(interval))
    subprocess.run(cmd, cwd=os.path.join(ROOT, "integrity", "pyhashv2"))


def main():
    parser = argparse.ArgumentParser(description="Unified Vault - host+network+file security monitoring")
    parser.add_argument("--mode", required=True, choices=["ips", "ids", "integrity", "all"])
    parser.add_argument("--baseline", metavar="PATH", help="Create integrity baseline for PATH")
    parser.add_argument("--audit", metavar="PATH", help="Audit PATH against saved baseline")
    parser.add_argument("--watch", metavar="PATH", help="Continuously audit PATH")
    parser.add_argument("--interval", type=int, default=30, help="Watch interval in seconds (default 30)")
    args = parser.parse_args()

    if args.mode == "ips":
        run_ips()
    elif args.mode == "ids":
        run_ids()
    elif args.mode == "integrity":
        if args.baseline:
            run_integrity("baseline", args.baseline)
        elif args.audit:
            run_integrity("audit", args.audit)
        elif args.watch:
            run_integrity("watch", args.watch, args.interval)
        else:
            parser.error("integrity mode requires --baseline, --audit, or --watch PATH")
    elif args.mode == "all":
        cfg = get_config()
        integrity_target = args.watch or cfg["integrity"]["scan_targets"][0]
        threads = [
            threading.Thread(target=run_ips, daemon=True),
            threading.Thread(target=run_ids, daemon=True),
            threading.Thread(target=run_integrity, args=("watch", integrity_target, args.interval), daemon=True),
        ]
        print(f"[*] Unified Vault online — IDS + IPS + integrity watch ({integrity_target}, every {args.interval}s)")
        for t in threads:
            t.start()
        try:
            while True:
                for t in threads:
                    t.join(timeout=1)
        except KeyboardInterrupt:
            print("\n[!] Shutting down Unified Vault...")


if __name__ == "__main__":
    main()
