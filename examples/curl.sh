#!/usr/bin/env bash
# Midjourney on APIMart: Imagine job -> poll -> upscale follow-up. Billed per call.
set -euo pipefail
: "${APIMART_API_KEY:?export APIMART_API_KEY first}"
BASE="${APIMART_BASE_URL:-https://api.apimart.ai/v1}"
AUTH=(-H "Authorization: Bearer $APIMART_API_KEY" -H 'Content-Type: application/json')
PROMPT="${1:-a curious tabby cat in a sunbeam, watercolor illustration --ar 16:9}"

echo "== submit Imagine job =="
TASK=$(curl -sS "$BASE/midjourney/generations" "${AUTH[@]}" \
  -d "$(python3 -c 'import json,sys; print(json.dumps({"prompt": sys.argv[1]}))' "$PROMPT")" \
  | python3 -c 'import json,sys; d=json.load(sys.stdin)["data"]; print(d["id"] if isinstance(d,dict) else d[0]["task_id"])')
echo "task: $TASK"

echo "== poll =="
for _ in $(seq 1 60); do
  RESPONSE=$(curl -sS "$BASE/tasks/$TASK" "${AUTH[@]}")
  STATUS=$(printf '%s' "$RESPONSE" | python3 -c 'import json,sys; print(json.load(sys.stdin)["data"]["status"])')
  echo "status: $STATUS"
  [ "$STATUS" = "completed" ] && break
  [ "$STATUS" = "failed" ] && { printf '%s\n' "$RESPONSE"; exit 1; }
  sleep 5
done
printf '%s' "$RESPONSE" | python3 -c 'import json,sys; d=json.load(sys.stdin)["data"]; print("cost:", d.get("cost"), "images:", d.get("result",{}).get("images",[{}])[0].get("url"))'

echo "== upscale image 1 (a new call, a new charge) =="
curl -sS "$BASE/midjourney/generations/upscale" "${AUTH[@]}" -d "{\"task_id\": \"$TASK\", \"index\": 1}" | head -c 300; echo
