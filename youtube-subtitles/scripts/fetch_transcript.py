#!/usr/bin/env python3
"""Download one video's captions and always save plain text.

The saved file is pure text: one caption line per line, UTF-8, no JSON, no
timestamps, no markup. The CLI's own ``text`` formatter cannot be relied on
across versions, so this wrapper asks for JSON (stable, documented) and strips
it down to plain text itself.

Usage:
    python fetch_transcript.py <video-id-or-url> [--out DIR] [--languages en]
                              [--exclude-generated] [--python PATH]
                              [--overwrite] [--print-text]

Exit codes: 0 saved, 2 no/blocked captions, 3 usage or environment error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
SCRIPT_DIR = Path(__file__).resolve().parent


class UsageError(Exception):
    """Raised for bad arguments; reported without a traceback."""


def extract_video_id(raw: str) -> str:
    """Return the 11-character video ID from an ID or a YouTube URL."""
    value = raw.strip().strip('"').strip("'")
    if value.startswith("\\-"):
        value = value[1:]
    if VIDEO_ID_RE.match(value):
        return value

    # URLs: youtu.be/ID, /watch?v=ID, /shorts/ID, /live/ID, /embed/ID
    patterns = (
        r"[?&]v=([A-Za-z0-9_-]{11})",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"/(?:shorts|live|embed|v)/([A-Za-z0-9_-]{11})",
    )
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    raise UsageError(f"cannot extract an 11-character video ID from {raw!r}")


def run_cli(python: str, args: list[str]) -> subprocess.CompletedProcess:
    cmd = [python, "-m", "youtube_transcript_api", *args]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        cwd=str(SCRIPT_DIR.parent),
    )


def parse_segments(stdout: str) -> list[dict]:
    """Parse the CLI's JSON output into caption segments.

    Requires the documented shape: objects carrying `text`, `start`, and
    `duration`. A single video's segment array may be wrapped in an outer list.
    """
    data = json.loads(stdout)
    if isinstance(data, list) and len(data) == 1 and isinstance(data[0], list):
        data = data[0]
    if not isinstance(data, list):
        raise ValueError("unexpected JSON shape")
    segments = [
        item for item in data
        if isinstance(item, dict)
        and isinstance(item.get("text"), str)
        and "start" in item
        and "duration" in item
    ]
    if not segments:
        raise ValueError("no caption segments with text/start/duration")
    return segments


def report_cli_failure(stdout: str, stderr: str) -> None:
    """Explain a failed CLI run without dressing it up as a success.

    Some CLI versions print a human-readable failure report to stdout and still
    exit 0, so a non-JSON payload is the real failure signal; only the diagnostic
    core of that report is echoed back, never its boilerplate.
    """
    print("error: no transcript returned", file=sys.stderr)
    reason = ""
    if stdout and not stdout.lstrip().startswith(("[", "{")):
        for line in stdout.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("Could not retrieve a transcript"):
                continue
            if stripped.startswith("If you are sure"):
                break
            reason = stripped
            break
    if reason:
        print(f"cli: {reason}", file=sys.stderr)
    if stderr:
        print(stderr, file=sys.stderr)


def segments_to_text(segments: list[dict]) -> str:
    """Join caption segments into plain lines, dropping repeated lines."""
    lines: list[str] = []
    for segment in segments:
        text = re.sub(r"\s+", " ", str(segment.get("text", ""))).strip()
        if not text:
            continue
        if lines and lines[-1] == text:
            continue
        lines.append(text)
    return "\n".join(lines) + "\n"


def list_language_codes(listing: str) -> tuple[list[str], list[str]]:
    """Split `--list-transcripts` output into (manual, generated) codes.

    The listing is human-readable text, not JSON, e.g.
    ` - en ("English")[TRANSLATABLE]`, under a `(MANUALLY CREATED)` heading and
    later a `(GENERATED)` heading. Auto-generated entries are listed with their
    own code in that section, so the section marker - not the entry text - decides
    which bucket a code lands in.
    """
    marker = re.compile(r"^\s*-\s+([A-Za-z][\w-]{0,15})\s+\(")
    manual: list[str] = []
    generated: list[str] = []
    section = "manual"
    for line in listing.splitlines():
        stripped = line.strip().upper()
        if stripped.startswith("(GENERATED"):
            section = "generated"
            continue
        if stripped.startswith("(MANUALLY CREATED"):
            section = "manual"
            continue
        if stripped.startswith("(TRANSLATION"):
            section = "translation"
            continue
        if section == "translation":
            continue
        match = marker.match(line)
        if match:
            code = match.group(1)
            if section == "generated":
                if code not in generated:
                    generated.append(code)
            elif code not in manual:
                manual.append(code)
    return manual, generated


def choose_language(listing: str, requested: list[str]) -> str:
    """Pick the language code that the download most plausibly used.

    Manually created code: the file is named after what YouTube itself reports,
    not after what was asked for, so an `en` request that resolved to `en-US`
    is labelled `en-US`.
    """
    manual, generated = list_language_codes(listing)
    wants = [want.lower() for want in requested]
    bases = [want.split("-")[0] for want in wants]
    for pool in (manual, generated):
        by_code = {code.lower(): code for code in pool}
        for want in wants:
            if want in by_code:
                return by_code[want]
        for code in pool:  # regional variant of a requested language
            lowered = code.lower()
            if any(lowered.startswith(want + "-") for want in wants) or lowered in bases:
                return code
    if manual:
        return manual[0]
    if generated:
        return generated[0]
    if len(requested) == 1:
        return requested[0]
    return "unknown"


def probe_language(python: str, video_id: str, requested: list[str]) -> str:
    """Best-effort language code for naming, from the listing; never fatal."""
    try:
        result = run_cli(python, ["--list-transcripts", video_id])
    except OSError:
        return requested[0] if len(requested) == 1 else "unknown"
    if result.returncode != 0:
        return requested[0] if len(requested) == 1 else "unknown"
    return choose_language(result.stdout, requested)


def unique_path(path: Path, overwrite: bool) -> Path:
    if overwrite or not path.exists():
        return path
    stem, suffix, parent = path.stem, path.suffix, path.parent
    index = 2
    while True:
        candidate = parent / f"{stem}.{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Save YouTube captions as plain text.")
    parser.add_argument("video", help="video ID or YouTube URL")
    parser.add_argument("--out", default="raw", help="output directory (default: raw)")
    parser.add_argument("--languages", default="en", help="comma-separated language codes")
    parser.add_argument("--exclude-generated", action="store_true",
                        help="manual captions only")
    parser.add_argument("--python", default=sys.executable, help="interpreter for the CLI")
    parser.add_argument("--overwrite", action="store_true", help="replace an existing file")
    parser.add_argument("--print-text", action="store_true",
                        help="also print the saved text to stdout")
    args = parser.parse_args(argv)

    try:
        video_id = extract_video_id(args.video)
    except UsageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    languages = [part.strip() for part in args.languages.split(",") if part.strip()]
    cli_args = [video_id, "--languages", *languages, "--format", "json"]
    if args.exclude_generated:
        cli_args.append("--exclude-generated")

    try:
        result = run_cli(args.python, cli_args)
    except FileNotFoundError:
        print(f"error: interpreter not found: {args.python}", file=sys.stderr)
        return 3
    except OSError as exc:
        print(f"error: cannot run the CLI: {exc}", file=sys.stderr)
        return 3

    stderr = (result.stderr or "").strip()
    stdout = (result.stdout or "").strip()
    if result.returncode != 0 or not stdout:
        report_cli_failure(stdout, stderr)
        return 2

    try:
        segments = parse_segments(stdout)
    except (ValueError, json.JSONDecodeError):
        report_cli_failure(stdout, stderr)
        return 2

    text = segments_to_text(segments)
    if not text.strip():
        print("error: no transcript returned (empty caption list)", file=sys.stderr)
        if stderr:
            print(stderr, file=sys.stderr)
        return 2

    language = probe_language(args.python, video_id, languages)
    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    target = unique_path(out_dir / f"{video_id}.{language}.txt", args.overwrite)
    target.write_text(text, encoding="utf-8", newline="\n")

    # Verify by reading back what was written.
    saved = target.read_text(encoding="utf-8")
    if not saved.strip():
        print("error: verification failed, saved file is empty", file=sys.stderr)
        return 2

    if args.print_text:
        sys.stdout.write(saved)
    print(f"saved: {target.resolve()}")
    print(f"language: {language}")
    print(f"format: text ({len(saved.splitlines())} lines, {len(saved)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
