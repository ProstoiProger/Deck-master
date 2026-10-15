SEVERITIES = ["Critical", "High", "Medium", "Low"]
RANK = {s: i for i, s in enumerate(SEVERITIES)}


def finding(sev, scene, msg):
    where = f"slide {scene.index} ({scene.layout})" if scene is not None else "deck"
    return f"[{sev}] {where}: {msg}"


def severity_of(text):
    if text.startswith("[") and "]" in text:
        sev = text[1:text.index("]")]
        if sev in RANK:
            return sev
    return "High"


def blocking(findings):
    """Critical and High findings stop a build."""
    return [f for f in findings if RANK[severity_of(f)] <= RANK["High"]]


def sort_findings(findings):
    return sorted(findings, key=lambda f: RANK[severity_of(f)])
