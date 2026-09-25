"""Exercise real fixture admission; no sockets, delays, or external services."""
import argparse
import json
from gateway import admit


def run(*, origin="local", requests=1, relay_active=True, relay_tag=True,
        access="clean"):
    admitted = sum(admit(origin=origin, relay_active=relay_active,
                         relay_tag=relay_tag, slot=i)
                   for i in range(1, requests + 1))
    # Independent access delay remains visible after an admission repair.
    late = admitted // 2 if origin == "client" and access == "noisy" else 0
    return {
        "entry": origin,
        "path": (["local", "service"] if origin == "local" else
                 ["client", "access", "relay", "admission", "service"]),
        "requests": requests,
        "relay_active": relay_active,
        "relay_tag": relay_tag,
        "access": access,
        "admission_dropped": requests - admitted,
        "delivered": admitted,
        "late": late,
        "within_deadline": admitted - late,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origin", choices=["local", "client"], default="local")
    parser.add_argument("--requests", type=int, choices=range(1, 33), default=1)
    parser.add_argument("--relay", choices=["on", "off"], default="on")
    parser.add_argument("--tag", choices=["on", "off"], default="on")
    parser.add_argument("--access", choices=["clean", "noisy"], default="clean")
    args = parser.parse_args()
    print(json.dumps(run(origin=args.origin, requests=args.requests,
                         relay_active=args.relay == "on", relay_tag=args.tag == "on",
                         access=args.access), sort_keys=True))


if __name__ == "__main__":
    main()
