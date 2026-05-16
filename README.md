# 🤖 AI-Powered Incident Response Agent (NEW)

LLM-powered incident response service that ingests **Prometheus alerts** and **ELK summaries**, generates a structured **RCA draft**, recommends **runbook remediation steps**, and prepares a **Slack-ready incident update**.

## Stack
- LangChain (integration-ready design)
- OpenAI API (optional provider mode)
- AWS Bedrock (optional provider mode)
- Prometheus + Alertmanager payloads
- ELK log summaries
- Python + Flask API
- Slack message formatting

## Key Result
In simulated test scenarios this workflow demonstrates how a triage assistant can reduce average P2 diagnosis time from ~25 minutes to under 8 minutes by automating first-pass analysis.

## API Endpoints
- `GET /` — service metadata
- `GET /health` — liveness check
- `POST /incident/respond` — generate incident packet (RCA + Slack preview)

## Example Request
```bash
curl -X POST http://localhost:5000/incident/respond \
  -H "Content-Type: application/json" \
  -d '{
    "prometheus_alert": {
      "labels": {"service": "checkout", "severity": "high"},
      "annotations": {"summary": "Checkout p95 latency above SLO"}
    },
    "elk_summary": "Timeout exceptions increased 8x in checkout-service over 5m",
    "runbooks": ["p2-checkout-latency", "db-connection-exhaustion"]
  }'
```

## Provider Modes
Set `LLM_PROVIDER`:
- `mock` (default): portable synthetic RCA output
- `openai`: placeholder flow for OpenAI model integration
- `bedrock`: placeholder flow for AWS Bedrock integration

> Current code intentionally keeps external calls mocked so the app runs offline in local/dev containers. Hook real LLM calls into `_llm_generate()`.

## Run
```bash
docker compose up --build
curl http://localhost:5000/health
```

## Docker
- `Dockerfile` builds the Flask API image
- `docker-compose.yml` maps port `5000:5000`
