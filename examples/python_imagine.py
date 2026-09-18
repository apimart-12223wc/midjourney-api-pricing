#!/usr/bin/env python3
"""Midjourney on APIMart: submit an Imagine job, poll it, and upscale one image.

Billing is per call: the Imagine job is one charge, each upscale is another.
"""

import argparse, os, pathlib, time
import requests

BASE = os.environ.get("APIMART_BASE_URL", "https://api.apimart.ai/v1")
HEADERS = {"Authorization": f"Bearer {os.environ['APIMART_API_KEY']}", "Content-Type": "application/json"}


def imagine(prompt: str) -> dict:
    created = requests.post(f"{BASE}/midjourney/generations", headers=HEADERS,
                            json={"prompt": prompt}, timeout=60)
    created.raise_for_status()
    data = created.json()["data"]
    task_id = data["id"] if isinstance(data, dict) else data[0]["task_id"]
    delay = 5
    for _ in range(90):
        task = requests.get(f"{BASE}/tasks/{task_id}", headers=HEADERS, timeout=60).json()["data"]
        if task["status"] in ("completed", "failed"):
            return task
        time.sleep(delay)
        delay = min(delay + 2, 15)
    raise TimeoutError(task_id)


def upscale(task_id: str, index: int = 1) -> dict:
    response = requests.post(f"{BASE}/midjourney/generations/upscale", headers=HEADERS,
                             json={"task_id": task_id, "index": index}, timeout=60)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Midjourney Imagine + upscale")
    ap.add_argument("--prompt", default="a curious tabby cat in a sunbeam, watercolor illustration --ar 16:9")
    ap.add_argument("--upscale", action="store_true", help="also upscale image 1 (a second billed call)")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()

    task = imagine(args.prompt)
    print(f"status={task['status']} cost={task.get('cost')} credits={task.get('credits_cost')}")
    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)
    for url in (task.get("result", {}).get("images", [{}])[0].get("url") or []):
        dest = pathlib.Path(args.out) / url.rsplit("/", 1)[-1]
        dest.write_bytes(requests.get(url, timeout=120).content)
        print("saved", dest)

    if args.upscale:
        print("upscale:", upscale(task["id"], 1))
