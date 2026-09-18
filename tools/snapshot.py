#!/usr/bin/env python3
"""Refresh Midjourney (midjourney) pricing from the public pricing payload.

    python tools/snapshot.py                # fetch the live pricing page
    python tools/snapshot.py --from-file p.html
    python tools/snapshot.py --check        # exit 1 when something moved (CI guard)
"""
from __future__ import annotations

import argparse, json, pathlib, re, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "model.json"
README = ROOT / "README.md"
PAGE = "https://apimart.ai/en/pricing"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36")
PRIMARY = "midjourney"
OFFICIAL = ""
TARGETS = [t for t in (PRIMARY, OFFICIAL) if t]


def fetch() -> str:
    cp = subprocess.run(["curl", "-sL", "-m", "45", "-H", f"User-Agent: {UA}", PAGE], capture_output=True, text=True)
    if not cp.stdout:
        raise SystemExit("failed to fetch the pricing page")
    return cp.stdout


def rsc_blob(html: str) -> str:
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)', html)
    return "".join(c.encode().decode("unicode_escape", errors="ignore") for c in chunks)


def records(text: str) -> dict:
    out, i = {}, 0
    while True:
        i = text.find('{"id":"', i)
        if i < 0:
            return out
        depth, j = 0, i
        while j < len(text):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        try:
            rec = json.loads(text[i:j + 1])
        except Exception:
            i = j + 1
            continue
        if rec.get("id") in TARGETS:
            out[rec["id"]] = rec
        i = j + 1


def money(v) -> str:
    if v in (None, ""):
        return "—"
    v = float(v)
    if v == 0:
        return "free"
    if v < 0.01:
        return f"${v:.6f}".rstrip("0").rstrip(".")
    if v < 1:
        return f"${v:.4f}".rstrip("0").rstrip(".")
    return f"${v:,.2f}"


def snapshot_of(rec: dict) -> dict:
    fixed = rec.get("fixed_prices") or {}
    pricing = rec.get("pricing") or {}
    if fixed.get("items"):
        return {"unit": fixed.get("unit"),
                "prices": {i["key"]: {"list": i.get("original_price"), "effective": i.get("after_discount")}
                           for i in fixed["items"]}}
    rates = pricing.get("effective_rates") or pricing.get("rates") or {}
    return {"unit": pricing.get("unit"), "prices": {"per_million_tokens": {"effective": rates}}} if rates else {}


def render(primary: dict, official: dict | None) -> str:
    rows = ["| Output | List price | Effective price |", "| --- | --- | --- |"]
    for key, cell in (snapshot_of(primary).get("prices") or {}).items():
        if isinstance(cell, dict) and ("list" in cell or "effective" in cell):
            rows.append(f"| {key} | {money(cell.get('list'))} | {money(cell.get('effective'))} |")
    body = "\n".join(rows)
    if official:
        rates = (snapshot_of(official).get("prices") or {}).get("per_million_tokens", {}).get("effective", {})
        if rates:
            body += "\n\nThe token-billed official route bills per million tokens instead: " + ", ".join(
                f"`{k}` {money(v)}" for k, v in rates.items()) + "."
    return body


def main() -> None:
    ap = argparse.ArgumentParser(description="Refresh Midjourney pricing")
    ap.add_argument("--from-file")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    html = pathlib.Path(args.from_file).read_text(errors="ignore") if args.from_file else fetch()
    found = records(rsc_blob(html))
    primary = found.get(PRIMARY)
    if not primary:
        raise SystemExit(f"model {PRIMARY} not present in the pricing payload")

    payload = {"id": PRIMARY, "alias": "", "official": OFFICIAL,
               "source": PAGE, "extracted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "prices": snapshot_of(primary).get("prices", {}),
               "official_prices": snapshot_of(found.get(OFFICIAL, {})).get("prices", {})}
    new_json = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    old_json = DATA.read_text() if DATA.exists() else ""
    if args.check:
        print("changed" if new_json != old_json else "unchanged")
        sys.exit(1 if new_json != old_json else 0)

    DATA.write_text(new_json)
    readme = README.read_text()
    start, end = "<!-- pricing:model:start -->", "<!-- pricing:model:end -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pattern.search(readme):
        raise SystemExit("pricing:model markers missing in README")
    README.write_text(pattern.sub(f"{start}\n{render(primary, found.get(OFFICIAL))}\n{end}", readme))
    print("pricing refreshed for", PRIMARY)


if __name__ == "__main__":
    main()
