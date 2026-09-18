# Midjourney API Pricing — Per-Call Cost With Worked Examples

What **Midjourney API pricing** actually looks like: a flat charge per call (Imagine, upscale, blend), how that differs from the subscription plans, and worked totals for 100 / 1,000 / 10,000 assets including the upscale step.

**Attributed entry points:** [Open Midjourney on APIMart](https://go.apimart.ai/k-e1468f) · [Current pricing](https://go.apimart.ai/k-36aff6) · [Get an API key](https://go.apimart.ai/k-ecfc07)

- Model id: `midjourney` (per-call billing)
- Endpoints: `POST /v1/midjourney/generations`, `POST /v1/midjourney/generations/upscale`, poll `GET /v1/tasks/{task_id}`
- Real jobs in this repository: **4**, total reported cost **$0.18016**

## Pricing per call

<!-- pricing:model:start -->
| Output | List price | Effective price |
| --- | --- | --- |
| default | $0.0563 | $0.045 |
| blend | $0.0688 | $0.055 |
| blend-fast | $0.0688 | $0.055 |
| blend-turbo | $0.125 | $0.1 |
| describe | $0.0688 | $0.055 |
| describe-fast | $0.0688 | $0.055 |
| describe-turbo | $0.125 | $0.1 |
| edits | $0.0688 | $0.055 |
| edits-fast | $0.0688 | $0.055 |
| edits-turbo | $0.125 | $0.1 |
| high_variation | $0.0688 | $0.055 |
| high_variation-fast | $0.0688 | $0.055 |
| high_variation-turbo | $0.125 | $0.1 |
| imagine | $0.0563 | $0.045 |
| imagine-fast | $0.0688 | $0.055 |
| imagine-niji6 | $0.0563 | $0.045 |
| imagine-niji6-fast | $0.0688 | $0.055 |
| imagine-niji6-turbo | $0.125 | $0.1 |
| imagine-niji7 | $0.0563 | $0.045 |
| imagine-niji7-fast | $0.0688 | $0.055 |
| imagine-niji7-turbo | $0.125 | $0.1 |
| imagine-turbo | $0.125 | $0.1 |
| imagine-v5.1 | $0.0563 | $0.045 |
| imagine-v5.1-fast | $0.0688 | $0.055 |
| imagine-v5.1-turbo | $0.125 | $0.1 |
| imagine-v5.2 | $0.0563 | $0.045 |
| imagine-v5.2-fast | $0.0688 | $0.055 |
| imagine-v5.2-turbo | $0.125 | $0.1 |
| imagine-v6.1 | $0.0563 | $0.045 |
| imagine-v6.1-fast | $0.0688 | $0.055 |
| imagine-v6.1-turbo | $0.125 | $0.1 |
| imagine-v7 | $0.0563 | $0.045 |
| imagine-v7-fast | $0.0688 | $0.055 |
| imagine-v7-turbo | $0.125 | $0.1 |
| imagine-v8.1 | $0.0563 | $0.045 |
| imagine-v8.1-fast | $0.0688 | $0.055 |
| imagine-v8.1-turbo | $0.125 | $0.1 |
| imagine-v8.2 | $0.0563 | $0.045 |
| imagine-v8.2-fast | $0.0688 | $0.055 |
| imagine-v8.2-turbo | $0.125 | $0.1 |
| inpaint | $0.0688 | $0.055 |
| inpaint-fast | $0.0688 | $0.055 |
| inpaint-turbo | $0.125 | $0.1 |
| low_variation | $0.0688 | $0.055 |
| low_variation-fast | $0.0688 | $0.055 |
| low_variation-turbo | $0.125 | $0.1 |
| modal | $0.0688 | $0.055 |
| modal-fast | $0.0688 | $0.055 |
| modal-turbo | $0.125 | $0.1 |
| pan | $0.0688 | $0.055 |
| pan-fast | $0.0688 | $0.055 |
| pan-turbo | $0.125 | $0.1 |
| remix_strong | $0.0688 | $0.055 |
| remix_strong-fast | $0.0688 | $0.055 |
| remix_strong-turbo | $0.125 | $0.1 |
| remix_subtle | $0.0688 | $0.055 |
| remix_subtle-fast | $0.0688 | $0.055 |
| remix_subtle-turbo | $0.125 | $0.1 |
| reroll | $0.0688 | $0.055 |
| reroll-fast | $0.0688 | $0.055 |
| reroll-turbo | $0.125 | $0.1 |
| shorten | $0.0688 | $0.055 |
| shorten-fast | $0.0688 | $0.055 |
| shorten-turbo | $0.125 | $0.1 |
| upscale | $0.0688 | $0.055 |
| upscale-fast | $0.0688 | $0.055 |
| upscale-turbo | $0.125 | $0.1 |
| variation | $0.0688 | $0.055 |
| variation-fast | $0.0688 | $0.055 |
| variation-turbo | $0.125 | $0.1 |
| video | $0.25 | $0.2 |
| video-720p | $0.5 | $0.4 |
| zoom | $0.0688 | $0.055 |
| zoom-fast | $0.0688 | $0.055 |
| zoom-turbo | $0.125 | $0.1 |
<!-- pricing:model:end -->

| Assets | Imagine only | With one upscale each |
| --- | --- | --- |
| 100 | $4.50 | $9.01 |
| 1,000 | $45.04 | $90.08 |
| 10,000 | $450.40 | $900.80 |

Each row is one call: an Imagine job is one charge, an upscale is another. The completed task reports the exact `cost`.

## Verified behaviour

| Capability | Verified behaviour |
| --- | --- |
| Imagine job | `POST /v1/midjourney/generations` with `{prompt}` returns a task id |
| Async polling | `GET /v1/tasks/{task_id}` reaches `completed` and reports `cost` in USD |
| Upscale follow-up | `POST /v1/midjourney/generations/upscale` with `{task_id, index}` returns a new task |
| Prompt flags | Midjourney flags such as `--ar 16:9` are passed through inside the prompt string |
| Moderation | new routes auto-inject moderation before submitting the job |

## Quickstart

```bash
# 1. submit an Imagine job (Midjourney flags go inside the prompt)
curl -sS https://api.apimart.ai/v1/midjourney/generations \
  -H "Authorization: Bearer $APIMART_API_KEY" -H 'Content-Type: application/json' \
  -d '{"prompt": "a curious tabby cat in a sunbeam, watercolor illustration --ar 16:9"}'

# 2. poll until status=completed (the payload carries cost and image URLs)
curl -sS https://api.apimart.ai/v1/tasks/task_01JWXXXX -H "Authorization: Bearer $APIMART_API_KEY"

# 3. upscale image 1 — a second billed call
curl -sS https://api.apimart.ai/v1/midjourney/generations/upscale \
  -H "Authorization: Bearer $APIMART_API_KEY" -H 'Content-Type: application/json' \
  -d '{"task_id": "task_01JWXXXX", "index": 1}'
```

```python
import os, requests

BASE = "https://api.apimart.ai/v1"
HEADERS = {"Authorization": f"Bearer {os.environ['APIMART_API_KEY']}", "Content-Type": "application/json"}
task = requests.post(f"{BASE}/midjourney/generations", headers=HEADERS, timeout=60,
                     json={"prompt": "a curious tabby cat in a sunbeam, watercolor illustration --ar 16:9"}).json()["data"]
print(task)   # -> task id; poll /tasks/<id> for status, cost and image URLs
```

Runnable versions (including the upscale follow-up) are in [`examples/`](examples).

## Outputs from real calls

| Output | Recipe | Calls | Cost | Prompt |
| --- | --- | --- | --- | --- |
| <img src="assets/02-product-cosmetics.jpg" width="220" alt="Midjourney output"> | Product ad | 1 Imagine | $0.04504 | `frosted glass serum bottle on wet pebbles, dramatic side light, shallow depth of field, commercial product photography --ar 1:1` |
| <img src="assets/01-watercolor-cat.jpg" width="220" alt="Midjourney output"> | Illustration | 1 Imagine | $0.04504 | `a curious tabby cat sitting in a sunbeam, soft watercolor illustration, loose brush strokes, warm palette --ar 16:9` |
| <img src="assets/03-cyberpunk-street.jpg" width="220" alt="Midjourney output"> | Cinematic | 1 Imagine | $0.04504 | `rainy neon alley in a cyberpunk city at night, reflections on wet asphalt, cinematic still, 35mm --ar 16:9` |
| <img src="assets/04-architectural-concept.jpg" width="220" alt="Midjourney output"> | Architecture | 1 Imagine | $0.04504 | `brutalist concrete pavilion beside a reflecting pool, overcast light, architectural photography, ultra sharp --ar 3:2` |

Prompts and the cost each job reported are also in [`data/samples.json`](data/samples.json).

## FAQ

**How is Midjourney billed on APIMart?**

Per call, not per token or per second: one Imagine job is one charge and each follow-up (upscale, variation, blend) is another. The pricing table above lists the effective price per call and the task reports the exact `cost`.

**How do I control the aspect ratio?**

Pass Midjourney flags inside the prompt, for example `--ar 16:9`. Everything after `--` is interpreted by the model rather than treated as scene description.

**What does an upscale cost?**

It is a separate call with its own charge. Budget one Imagine call plus one upscale call per final asset if that is your workflow.

**Is the official Midjourney subscription enough for API use?**

No — the subscription covers the Discord/web product. API access is a separate route, which is why the request shapes and the per-call price matter more than the plan price.

## Related searches

- `midjourney api pricing`
- `midjourney api cost`
- `midjourney api`
- `image generation api pricing`
- `per call api pricing`
- `cheap image api`
- `ai image api`

## Attributed links (how this repository is measured)

| Purpose | Attributed link | Target |
| --- | --- | --- |
| Open Midjourney on APIMart | <https://go.apimart.ai/k-e1468f> | `apimart.ai/model/midjourney` |
| Current pricing page | <https://go.apimart.ai/k-36aff6> | `apimart.ai/pricing` |
| Get an API key | <https://go.apimart.ai/k-ecfc07> | `apimart.ai/keys` |

Outbound APIMart links are minted through the promo link API; hand-made tracking parameters are rejected by
`tools/check_links.py` in CI.

## Disclosure

Midjourney is a third-party product served here through a relay route; this repository documents how to call it and
publishes real outputs and per-call prices, and does not claim official status or affiliation. Product names,
documentation and generated media belong to their owners. Endpoint reference:
[https://docs.apimart.ai/en/api-reference/images/midjourney/generation](https://docs.apimart.ai/en/api-reference/images/midjourney/generation).

## Repository map

```text
README.md             access path, per-call pricing, verified behaviour, real outputs
data/model.json       per-call price cells (CI-refreshed)
data/samples.json     real jobs with prompts and reported cost
tools/snapshot.py     refresh pricing from the public payload
tools/check_links.py  attribution guard
examples/             curl and Python clients (Imagine + upscale)
assets/               real outputs (JPEG, resized for the README)
.github/workflows/    daily price refresh + validation
```

## License

MIT — see [LICENSE](LICENSE).
