#!/usr/bin/env python3
"""
Analyze Claude Code session logs to extract token usage and estimate costs.

Usage:
  python3 token_cost.py [--session current|last|all|SESSION_ID] [--project PROJECT_PATH]

Defaults: --session current, --project auto-detected from cwd.
"""

import json
import os
import re
import sys
import argparse
import urllib.request
from pathlib import Path
from datetime import datetime


def is_noise(text: str) -> bool:
    """Filter out system-generated noise from user messages."""
    noise_patterns = [
        "(no text)",
        "[Request interrupted",
        "Base directory for this skill:",
        "<command-name>",
        "<local-command-",
        "<bash-input>",
        "<bash-stdout>",
        "<bash-stderr>",
        "<task-notification>",
    ]
    text_lower = text.strip().lower()
    if not text_lower or len(text_lower) < 3:
        return True
    for pattern in noise_patterns:
        if pattern.lower() in text_lower:
            return True
    return False


def get_project_key(project_path: str) -> str:
    """Convert project path to Claude's directory key format."""
    return project_path.replace("/", "-")


def detect_project_path() -> str:
    """Auto-detect current project path from cwd."""
    return os.getcwd()


def get_sessions_dir(project_path: str) -> Path:
    """Get the Claude sessions directory for a project."""
    key = get_project_key(project_path)
    return Path.home() / ".claude" / "projects" / key


def list_session_files(sessions_dir: Path) -> list[Path]:
    """List all session JSONL files sorted by modification time (newest first)."""
    if not sessions_dir.exists():
        return []
    files = [f for f in sessions_dir.glob("*.jsonl") if f.is_file()]
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files


def get_current_session_id() -> str | None:
    """Try to get the current session ID from environment or session stats."""
    stats_file = Path.home() / ".claude" / ".session-stats.json"
    if stats_file.exists():
        try:
            data = json.loads(stats_file.read_text())
            return data.get("sessionId")
        except (json.JSONDecodeError, KeyError):
            pass
    return None


def parse_session(filepath: Path) -> dict:
    """Parse a session JSONL file and extract token usage data."""
    result = {
        "session_id": filepath.stem,
        "file": str(filepath),
        "models": {},
        "total_input": 0,
        "total_output": 0,
        "total_cache_read": 0,
        "total_cache_write": 0,
        "message_count": 0,
        "assistant_turns": 0,
        "first_timestamp": None,
        "last_timestamp": None,
        "first_user_message": None,
        "user_messages": [],
    }

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            entry_type = entry.get("type")
            timestamp = entry.get("timestamp")

            if timestamp:
                if result["first_timestamp"] is None:
                    result["first_timestamp"] = timestamp
                result["last_timestamp"] = timestamp

            if entry_type == "user":
                msg = entry.get("message", {})
                content = msg.get("content", "")
                if isinstance(content, list):
                    text_parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
                    content = " ".join(text_parts)
                content = re.sub(r"<[^>]+>.*?</[^>]+>", "", content, flags=re.DOTALL).strip()
                if content and not is_noise(content):
                    result["user_messages"].append({
                        "timestamp": timestamp,
                        "text": content[:200]
                    })
                    if result["first_user_message"] is None:
                        result["first_user_message"] = content[:120]

            if entry_type == "assistant":
                result["assistant_turns"] += 1
                msg = entry.get("message", {})
                usage = msg.get("usage", {})
                model = msg.get("model", "unknown")

                input_tokens = usage.get("input_tokens", 0)
                output_tokens = usage.get("output_tokens", 0)
                cache_read = usage.get("cache_read_input_tokens", 0)
                cache_write = usage.get("cache_creation_input_tokens", 0)

                result["total_input"] += input_tokens
                result["total_output"] += output_tokens
                result["total_cache_read"] += cache_read
                result["total_cache_write"] += cache_write

                if model not in result["models"]:
                    result["models"][model] = {
                        "input": 0, "output": 0,
                        "cache_read": 0, "cache_write": 0,
                        "turns": 0
                    }
                result["models"][model]["input"] += input_tokens
                result["models"][model]["output"] += output_tokens
                result["models"][model]["cache_read"] += cache_read
                result["models"][model]["cache_write"] += cache_write
                result["models"][model]["turns"] += 1

            result["message_count"] += 1

    return result


def fetch_pricing() -> dict:
    """Fetch model pricing from models.dev API."""
    try:
        req = urllib.request.Request(
            "https://models.dev/api.json",
            headers={"User-Agent": "token-cost-skill/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        pricing = {}
        anthropic = data.get("anthropic", {})
        models = anthropic.get("models", {})
        for model_id, m in models.items():
            cost = m.get("cost", {}) if isinstance(m, dict) else {}
            if cost:
                pricing[model_id] = {
                    "input": cost.get("input", 0),
                    "output": cost.get("output", 0),
                    "cache_read": cost.get("cache_read", 0),
                    "cache_write": cost.get("cache_write", 0),
                }
        return pricing
    except Exception as e:
        print(f"  (No se pudieron obtener precios: {e})", file=sys.stderr)
        return {}


def calculate_cost(model_usage: dict, pricing: dict) -> float:
    """Calculate cost in USD for a model's token usage."""
    cost = 0.0
    for model, usage in model_usage.items():
        p = None
        # Try exact match first, then prefix match
        if model in pricing:
            p = pricing[model]
        else:
            for pid in pricing:
                if model.startswith(pid) or pid.startswith(model):
                    p = pricing[pid]
                    break
        if p:
            cost += (usage["input"] / 1_000_000) * p["input"]
            cost += (usage["output"] / 1_000_000) * p["output"]
            cost += (usage["cache_read"] / 1_000_000) * p["cache_read"]
            cost += (usage["cache_write"] / 1_000_000) * p["cache_write"]
    return cost


def format_number(n: int) -> str:
    """Format number with thousand separators."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def format_duration(start: str, end: str) -> str:
    """Calculate and format duration between two ISO timestamps."""
    try:
        t1 = datetime.fromisoformat(start.replace("Z", "+00:00"))
        t2 = datetime.fromisoformat(end.replace("Z", "+00:00"))
        delta = t2 - t1
        total_seconds = int(delta.total_seconds())
        if total_seconds < 60:
            return f"{total_seconds}s"
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        if minutes < 60:
            return f"{minutes}m {seconds}s"
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}m"
    except Exception:
        return "?"


def aggregate_sessions(session_files: list[Path]) -> dict:
    """Parse all sessions and return aggregated data plus per-session summaries."""
    totals = {
        "models": {},
        "total_input": 0,
        "total_output": 0,
        "total_cache_read": 0,
        "total_cache_write": 0,
        "assistant_turns": 0,
        "session_count": 0,
        "sessions": [],
        "first_timestamp": None,
        "last_timestamp": None,
    }

    for f in session_files:
        s = parse_session(f)
        if s["assistant_turns"] == 0:
            continue

        totals["session_count"] += 1
        totals["assistant_turns"] += s["assistant_turns"]
        totals["total_input"] += s["total_input"]
        totals["total_output"] += s["total_output"]
        totals["total_cache_read"] += s["total_cache_read"]
        totals["total_cache_write"] += s["total_cache_write"]

        for model, usage in s["models"].items():
            if model not in totals["models"]:
                totals["models"][model] = {
                    "input": 0, "output": 0,
                    "cache_read": 0, "cache_write": 0,
                    "turns": 0
                }
            for k in ("input", "output", "cache_read", "cache_write", "turns"):
                totals["models"][model][k] += usage[k]

        if s["first_timestamp"]:
            if totals["first_timestamp"] is None or s["first_timestamp"] < totals["first_timestamp"]:
                totals["first_timestamp"] = s["first_timestamp"]
        if s["last_timestamp"]:
            if totals["last_timestamp"] is None or s["last_timestamp"] > totals["last_timestamp"]:
                totals["last_timestamp"] = s["last_timestamp"]

        totals["sessions"].append(s)

    # Sort sessions by first_timestamp (oldest first)
    totals["sessions"].sort(key=lambda x: x["first_timestamp"] or "")

    return totals


def print_all_report(data: dict, pricing: dict, detail: bool = False):
    """Print aggregated report for all sessions in a project."""
    print()
    print("=" * 56)
    print("  PROJECT TOKEN USAGE (ALL SESSIONS)")
    print("=" * 56)
    print(f"  Sessions: {data['session_count']}")
    print(f"  Turns:    {data['assistant_turns']}")

    if data["first_timestamp"] and data["last_timestamp"]:
        try:
            t1 = datetime.fromisoformat(data["first_timestamp"].replace("Z", "+00:00"))
            t2 = datetime.fromisoformat(data["last_timestamp"].replace("Z", "+00:00"))
            print(f"  From:     {t1.strftime('%Y-%m-%d %H:%M')}")
            print(f"  To:       {t2.strftime('%Y-%m-%d %H:%M')}")
        except Exception:
            pass

    print("-" * 56)

    # Per-model breakdown
    for model, usage in data["models"].items():
        print(f"\n  Model: {model} ({usage['turns']} turns)")
        print(f"    Input tokens:       {format_number(usage['input']):>10}")
        print(f"    Output tokens:      {format_number(usage['output']):>10}")
        print(f"    Cache read tokens:  {format_number(usage['cache_read']):>10}")
        print(f"    Cache write tokens: {format_number(usage['cache_write']):>10}")

    # Totals
    total_all = (data["total_input"] + data["total_output"]
                 + data["total_cache_read"] + data["total_cache_write"])
    print()
    print("-" * 56)
    print(f"  TOTALS")
    print(f"    Input:        {format_number(data['total_input']):>10}")
    print(f"    Output:       {format_number(data['total_output']):>10}")
    print(f"    Cache read:   {format_number(data['total_cache_read']):>10}")
    print(f"    Cache write:  {format_number(data['total_cache_write']):>10}")
    print(f"    ALL tokens:   {format_number(total_all):>10}")

    # Cost estimate
    if pricing:
        cost = calculate_cost(data["models"], pricing)
        print()
        print(f"  Estimated cost: ${cost:.4f} USD")
        if cost > 0:
            for model, usage in data["models"].items():
                model_cost = calculate_cost({model: usage}, pricing)
                if model_cost > 0:
                    print(f"    {model}: ${model_cost:.4f}")

    # Per-session summary table
    print()
    print("-" * 56)
    print(f"  PER-SESSION BREAKDOWN")
    print(f"  {'Date':<18} {'Turns':>5} {'Tokens':>9} {'Cost':>10}  Task")
    print(f"  {'-'*17} {'-'*5} {'-'*9} {'-'*10}  {'-'*15}")

    for s in data["sessions"]:
        date_str = ""
        if s["first_timestamp"]:
            try:
                t = datetime.fromisoformat(s["first_timestamp"].replace("Z", "+00:00"))
                date_str = t.strftime("%Y-%m-%d %H:%M")
            except Exception:
                date_str = "?"

        total = s["total_input"] + s["total_output"] + s["total_cache_read"] + s["total_cache_write"]
        session_cost = calculate_cost(s["models"], pricing) if pricing else 0

        task = s.get("first_user_message", "") or ""
        if len(task) > 30:
            task = task[:30] + "..."

        cost_str = f"${session_cost:.4f}" if pricing else "-"
        print(f"  {date_str:<18} {s['assistant_turns']:>5} {format_number(total):>9} {cost_str:>10}  {task}")

        if detail and s.get("user_messages"):
            for msg in s["user_messages"]:
                text = msg["text"]
                if len(text) > 70:
                    text = text[:70] + "..."
                print(f"      > {text}")
            print()

    print("=" * 56)
    print()


def print_report(session: dict, pricing: dict, detail: bool = False):
    """Print a formatted token usage report."""
    print()
    print("=" * 56)
    print("  TOKEN USAGE REPORT")
    print("=" * 56)

    if session["first_user_message"]:
        label = session["first_user_message"]
        if len(label) > 50:
            label = label[:50] + "..."
        print(f"  Task:     {label}")

    if session["first_timestamp"] and session["last_timestamp"]:
        duration = format_duration(session["first_timestamp"], session["last_timestamp"])
        try:
            start = datetime.fromisoformat(session["first_timestamp"].replace("Z", "+00:00"))
            print(f"  Date:     {start.strftime('%Y-%m-%d %H:%M')}")
        except Exception:
            pass
        print(f"  Duration: {duration}")

    print(f"  Turns:    {session['assistant_turns']}")
    print("-" * 56)

    # Per-model breakdown
    for model, usage in session["models"].items():
        print(f"\n  Model: {model} ({usage['turns']} turns)")
        print(f"    Input tokens:       {format_number(usage['input']):>10}")
        print(f"    Output tokens:      {format_number(usage['output']):>10}")
        print(f"    Cache read tokens:  {format_number(usage['cache_read']):>10}")
        print(f"    Cache write tokens: {format_number(usage['cache_write']):>10}")

    # Totals
    total_all = (session["total_input"] + session["total_output"]
                 + session["total_cache_read"] + session["total_cache_write"])
    print()
    print("-" * 56)
    print(f"  TOTALS")
    print(f"    Input:        {format_number(session['total_input']):>10}")
    print(f"    Output:       {format_number(session['total_output']):>10}")
    print(f"    Cache read:   {format_number(session['total_cache_read']):>10}")
    print(f"    Cache write:  {format_number(session['total_cache_write']):>10}")
    print(f"    ALL tokens:   {format_number(total_all):>10}")

    # Cost estimate
    if pricing:
        cost = calculate_cost(session["models"], pricing)
        print()
        print(f"  Estimated cost: ${cost:.4f} USD")
        if cost > 0:
            # Per-model cost breakdown
            for model, usage in session["models"].items():
                model_cost = calculate_cost({model: usage}, pricing)
                if model_cost > 0:
                    print(f"    {model}: ${model_cost:.4f}")

    if detail and session.get("user_messages"):
        print()
        print("-" * 56)
        print("  USER PROMPTS")
        for i, msg in enumerate(session["user_messages"], 1):
            ts = ""
            if msg.get("timestamp"):
                try:
                    t = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
                    ts = t.strftime("%H:%M")
                except Exception:
                    pass
            text = msg["text"]
            if len(text) > 80:
                text = text[:80] + "..."
            print(f"  [{ts}] {text}")

    print("=" * 56)
    print()


def main():
    parser = argparse.ArgumentParser(description="Analyze Claude Code token usage")
    parser.add_argument(
        "--session", "-s",
        default="current",
        help="Session to analyze: 'current', 'last', 'all', or a session UUID (default: current)"
    )
    parser.add_argument(
        "--project", "-p",
        default=None,
        help="Project path (default: auto-detect from cwd)"
    )
    parser.add_argument(
        "--detail", "-d",
        action="store_true",
        default=False,
        help="Show detailed user prompts per session"
    )
    args = parser.parse_args()

    project_path = args.project or detect_project_path()
    sessions_dir = get_sessions_dir(project_path)

    if not sessions_dir.exists():
        print(f"Error: No sessions found for project {project_path}", file=sys.stderr)
        print(f"  Looked in: {sessions_dir}", file=sys.stderr)
        sys.exit(1)

    session_files = list_session_files(sessions_dir)
    if not session_files:
        print(f"Error: No session files found in {sessions_dir}", file=sys.stderr)
        sys.exit(1)

    pricing = fetch_pricing()

    # Handle "all" mode
    if args.session == "all":
        data = aggregate_sessions(session_files)
        if data["session_count"] == 0:
            print("No sessions with assistant messages found.")
            sys.exit(0)
        print_all_report(data, pricing, detail=args.detail)
        sys.exit(0)

    # Select session file
    target_file = None

    if args.session == "current":
        current_id = get_current_session_id()
        if current_id:
            for f in session_files:
                if f.stem == current_id:
                    target_file = f
                    break
        if target_file is None:
            target_file = session_files[0]
            print(f"  (Using most recent session as fallback)")

    elif args.session == "last":
        if len(session_files) >= 2:
            target_file = session_files[1]
        else:
            target_file = session_files[0]
            print(f"  (Only one session found)")

    else:
        for f in session_files:
            if f.stem == args.session:
                target_file = f
                break
        if target_file is None:
            print(f"Error: Session {args.session} not found", file=sys.stderr)
            sys.exit(1)

    # Parse and report
    session_data = parse_session(target_file)

    if session_data["assistant_turns"] == 0:
        print("No assistant messages found in this session.")
        sys.exit(0)

    print_report(session_data, pricing, detail=args.detail)


if __name__ == "__main__":
    main()
