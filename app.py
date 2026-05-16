import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List

from flask import Flask, jsonify, request

app = Flask(__name__)


def _severity_to_priority(severity: str) -> str:
    mapping = {
        "critical": "P1",
        "high": "P2",
        "warning": "P3",
        "info": "P4",
    }
    return mapping.get(severity.lower(), "P3")


def _build_prompt(alert: Dict[str, Any], elk_summary: str, runbooks: List[str]) -> str:
    return (
        "You are an incident commander assistant. Produce strict JSON with keys: "
        "incident_summary, likely_root_causes, evidence, remediation_steps, confidence_score.\n"
        f"Alert payload: {json.dumps(alert)}\n"
        f"ELK summary: {elk_summary}\n"
        f"Available runbooks: {json.dumps(runbooks)}"
    )


def _llm_generate(prompt: str) -> Dict[str, Any]:
    provider = os.getenv("LLM_PROVIDER", "mock").lower()

    # In this starter project we keep external calls optional for local portability.
    if provider in {"openai", "bedrock"}:
        model = os.getenv("LLM_MODEL", "gpt-4o-mini") if provider == "openai" else os.getenv("BEDROCK_MODEL", "anthropic.claude-3-5-sonnet")
        return {
            "incident_summary": f"LLM provider '{provider}' configured with model '{model}'.",
            "likely_root_causes": [
                "CPU saturation on checkout service",
                "Connection pool exhaustion in downstream datastore",
            ],
            "evidence": [
                "Prometheus high_latency and high_error_rate alerts triggered",
                "ELK logs show repeated timeout exceptions",
            ],
            "remediation_steps": [
                "Scale checkout deployment by +2 replicas",
                "Recycle stale DB connections and increase max pool size",
                "Run the checkout-latency P2 runbook",
            ],
            "confidence_score": 0.78,
            "note": "Template response. Plug LangChain chain invocation here for live LLM output.",
        }

    return {
        "incident_summary": "Synthetic RCA draft generated from alert + logs.",
        "likely_root_causes": [
            "Traffic spike caused checkout service CPU throttling",
            "Downstream datastore latency increased error budget burn",
        ],
        "evidence": [
            "Alert labels indicate service=checkout severity=high",
            "Log summary includes timeout + retry storm patterns",
        ],
        "remediation_steps": [
            "Throttle non-critical background jobs",
            "Scale deployment and restart unhealthy pods",
            "Execute runbook: p2-checkout-latency",
        ],
        "confidence_score": 0.73,
        "note": "Running in mock mode. Set LLM_PROVIDER=openai|bedrock for real integrations.",
    }


def _format_slack_message(incident: Dict[str, Any], rca: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "channel": os.getenv("SLACK_CHANNEL", "#incident-response"),
        "text": f"🚨 {incident['priority']} incident detected for {incident['service']}",
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*Incident:* {incident['title']}"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*RCA Draft:* {rca['incident_summary']}"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Top remediation steps:*\n"
                    + "\n".join([f"• {step}" for step in rca["remediation_steps"][:3]]),
                },
            },
        ],
    }


@app.route("/")
def home():
    return jsonify(
        {
            "name": "AI-Powered Incident Response Agent",
            "status": "running",
            "endpoints": ["/health", "/incident/respond"],
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()})


@app.route("/incident/respond", methods=["POST"])
def incident_respond():
    payload = request.get_json(silent=True) or {}

    alert = payload.get("prometheus_alert", {})
    elk_summary = payload.get("elk_summary", "No log summary provided")
    runbooks = payload.get("runbooks", ["p2-checkout-latency", "db-connection-exhaustion"])

    service = alert.get("labels", {}).get("service", "unknown-service")
    severity = alert.get("labels", {}).get("severity", "warning")

    incident = {
        "title": alert.get("annotations", {}).get("summary", "Service degradation detected"),
        "service": service,
        "severity": severity,
        "priority": _severity_to_priority(severity),
        "detected_at": datetime.now(timezone.utc).isoformat(),
    }

    prompt = _build_prompt(alert, elk_summary, runbooks)
    rca = _llm_generate(prompt)
    slack_payload = _format_slack_message(incident, rca)

    return jsonify(
        {
            "incident": incident,
            "rca_draft": rca,
            "slack_preview": slack_payload,
            "integration_notes": {
                "langchain": "Add a RunnableSequence and output parser around _build_prompt/_llm_generate.",
                "bedrock": "Use boto3 bedrock-runtime invoke_model or Converse API.",
                "openai": "Use OpenAI Responses API with JSON schema mode.",
            },
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
