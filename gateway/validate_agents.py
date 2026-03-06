"""
Phase 1 Validation Script — LiteLLM SDK + Ollama Connectivity

Tests that the LiteLLM SDK can reach each Ollama cloud-tunneled model
directly (no proxy server required). Maps the same virtual model roles
defined in litellm_config.yaml to actual Ollama model names.

Usage:
    python gateway/validate_agents.py

Prerequisites:
    - Ollama running locally on port 11434
    - cloud-tunneled models pulled (see: ollama list)
"""

import os
import sys
import time

import litellm
from dotenv import load_dotenv

load_dotenv()

# Disable LiteLLM's verbose logging for cleaner output
litellm.suppress_debug_info = True
litellm.set_verbose = False

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# ── Primary models (OpenRouter — verified March 2026) ──────────────────────
PRIMARY_MODELS = [
    (
        "intent-model [primary]",
        "openrouter/google/gemini-2.5-flash",
        "Reply ONE word (feature/bug/question): 'Add a login page'",
    ),
    (
        "worker-model [primary]",
        "openrouter/mistralai/ministral-8b-2512",
        "Reply with ONE word: what color is the sky?",
    ),
    (
        "developer-model [primary]",
        "openrouter/qwen/qwen-2.5-coder-32b-instruct",
        "Write a one-line Python lambda that adds two numbers.",
    ),
    (
        "architect-model [primary]",
        "openrouter/moonshotai/kimi-k2",
        "Name ONE clean architecture principle in 5 words.",
    ),
    (
        "critic-model [primary]",
        "openrouter/google/gemini-2.5-flash",
        "Give the most important code review rule in one sentence.",
    ),
]

# ── Fallback models ────────────────────────────────────────────────────────
FALLBACK_MODELS = [
    # intent fallbacks
    (
        "intent-model [fallback-1]",
        "ollama/gemini-3-flash-preview:cloud",
        "Classify in ONE word (feature/bug/question): 'Fix the login bug'",
    ),
    (
        "intent-model [fallback-2]",
        "openrouter/mistralai/ministral-3b-2512",
        "Classify in ONE word (feature/bug/question): 'Refactor auth module'",
    ),
    # worker fallback
    (
        "worker-model [fallback]",
        "ollama/ministral-3:8b-cloud",
        "Reply with ONE word: what color is grass?",
    ),
    # developer fallbacks
    (
        "developer-model [fallback-1]",
        "ollama/qwen3-coder-next:cloud",
        "Write a one-line Python lambda that multiplies two numbers.",
    ),
    (
        "developer-model [fallback-2]",
        "ollama/ministral-3:14b-cloud",
        "Write a one-line Python lambda that squares a number.",
    ),
    # architect fallbacks
    (
        "architect-model [fallback-1]",
        "openrouter/qwen/qwen-plus",
        "Name ONE SOLID principle in 5 words.",
    ),
    (
        "architect-model [fallback-2]",
        "ollama/qwen3.5:397b-cloud",
        "Name ONE DDD principle in 5 words.",
    ),
    # critic fallbacks
    (
        "critic-model [fallback-1]",
        "openrouter/minimax/minimax-m2.5",
        "Give the most important security review rule in one sentence.",
    ),
    (
        "critic-model [fallback-2]",
        "ollama/qwen3.5:397b-cloud",
        "Give the most important performance review rule in one sentence.",
    ),
]

MODELS_TO_TEST = PRIMARY_MODELS + FALLBACK_MODELS







def call_model(
    role: str, model: str, prompt: str
) -> tuple[bool, str, float]:
    """Call an Ollama model via the LiteLLM SDK. Returns (ok, text_or_error, latency)."""
    start = time.monotonic()
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            api_base=OLLAMA_BASE_URL,
            max_tokens=128,
            stream=False,
            timeout=120,
        )
        latency = time.monotonic() - start
        content = response.choices[0].message.content.strip()
        return True, content, latency
    except Exception as exc:
        return False, str(exc)[:200], time.monotonic() - start


def main() -> None:
    print("\n" + "═" * 64)
    print("  SaaS Assistant — Phase 1 Model Validation (LiteLLM SDK)")
    print("═" * 64)
    print(f"  Ollama endpoint : {OLLAMA_BASE_URL}")
    print("═" * 64 + "\n")

    results = []
    for role, model, prompt in MODELS_TO_TEST:
        print(f"  ⏳  [{role}]  →  {model}")
        ok, text, latency = call_model(role, model, prompt)
        status = "✅" if ok else "❌"
        lat_str = f"{latency:.1f}s"
        if ok:
            preview = text[:80] + ("…" if len(text) > 80 else "")
            print(f"  {status}  {role:20s} ({lat_str})  →  \"{preview}\"")
        else:
            print(f"  {status}  {role:20s} ({lat_str})  →  ERROR: {text}")
        results.append((role, ok, latency))
        print()

    print("─" * 64)
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    avg_lat = sum(lat for _, _, lat in results) / total

    print(f"  Result : {passed}/{total} models passed  |  avg latency {avg_lat:.1f}s")
    if passed == total:
        print("  🎉  Phase 1 COMPLETE — all virtual model IDs are reachable via Ollama!")
    else:
        print("  ⚠️   Some models failed. Check: ollama list")
    print("─" * 64 + "\n")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
