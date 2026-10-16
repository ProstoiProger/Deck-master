"""Number parsing shared by layouts and charts."""
import re


_THOUSANDS = re.compile(r"(?<![\d.,])(-?[1-9]\d{0,2}(?:[, ]\d{3})+)(?:[.,]\d+)?(?!\d)")
_PLAIN = re.compile(r"-?\d+(?:[.,]\d+)?")


def number(text):
    """First number in text as a float, or None. `48,000` and `48 000` are thousands; `0,5` and `3,25` are decimals."""
    s = str(text)
    m = _THOUSANDS.search(s)
    if m:
        whole = re.sub(r"[, ]", "", m.group(1))
        tail = s[m.end(1):m.end()]
        return float(whole + tail.replace(",", ".")) if tail else float(whole)
    m = _PLAIN.search(s.replace(" ", ""))
    return float(m.group(0).replace(",", ".")) if m else None
