import json
import time
from pathlib import Path


def log_run(path, **fields):
    """Append one JSON line per build; the log is the audit trail for what was delivered."""
    record = {"logged_at": time.strftime("%Y-%m-%dT%H:%M:%S"), **fields}
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, default=str, ensure_ascii=False) + "\n")
    return record


def read_runs(path):
    p = Path(path)
    if not p.exists():
        return []
    return [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
