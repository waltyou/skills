---
name: youtube-subtitles
description: Download YouTube subtitles when the user provides a video URL and asks to download or save captions/transcripts (下载字幕). Install or repair the youtube-transcript-api CLI when needed. Default to English, save plain-text .txt files under the current workspace's raw directory, and automatically provide a brief summary after a successful download.
---

# YouTube subtitles

Use `youtube-transcript-api` to retrieve existing YouTube captions, then automatically summarize the verified transcript in the same response. Explicit user language, format, destination, and summary preferences override the defaults below.

## Install and verify

Find a usable Python interpreter (`python`, `python3`, or `py`). Check `python -m youtube_transcript_api --version` and `--help`. Prefer the module invocation when the console executable is outside PATH.

If missing, install from PyPI using that same interpreter:

```sh
python -m pip install --user --upgrade youtube-transcript-api
python -m youtube_transcript_api --version
```

Inside an existing virtual environment omit `--user`. If the system Python is externally managed, use an isolated user-level virtual environment. Upgrade a working installation only when requested or needed to fix a demonstrated compatibility failure. Follow the host's normal execution permissions.

## Download

Default output is a plain-text `.txt` file: one caption line per line, UTF-8, no JSON, no timestamps, no markup. JSON is a transport detail of the CLI, not a deliverable — never save it as the transcript file.

Only an explicit user request changes that: for timestamps ask for `--format srt` (`.srt`), `--format webvtt` (`.vtt`), or `--format json` (`.json`), run the CLI directly, and keep the requested extension in the filename.

1. Resolve the active workspace/project root and read applicable local instructions. Default destination is `<workspace>/raw`, never the global skill directory. Create it when a download succeeds. Honor a destination the user explicitly provides.
2. Accept either a video ID or a URL. Extract the ID from `youtube.com/watch?v=...`, `youtu.be/...`, or YouTube `/shorts/`, `/live/`, and `/embed/` URLs. Ignore tracking parameters. Validate an 11-character ID containing letters, digits, `_`, or `-`. Treat a link with both `v` and `list` as one video unless a playlist is requested.
3. Default language is `en`. Prefer manual English captions, falling back to automatically generated English captions. If `en` is unavailable, list tracks and select an available English variant such as `en-US` or `en-GB`. For an explicit manual-only request use `--exclude-generated`. Never silently substitute another language or auto-translate. If no English track exists, report available languages; translate only when requested.
4. Name the file `<video-id>.<actual-language-code>.txt`. Preserve subtitle wording; keep summaries separate. Do not collapse lines into paragraphs and do not strip `[Music]` or `[Applause]` markers unless the user asks for that.

### Use the bundled wrapper

`scripts/fetch_transcript.py` (relative to this skill's base directory) runs the CLI and writes the plain-text file, so the CLI's own `text` formatter is never relied on:

```sh
python "<skill-dir>/scripts/fetch_transcript.py" "https://www.youtube.com/watch?v=VIDEO_ID" --out raw
python "<skill-dir>/scripts/fetch_transcript.py" VIDEO_ID --out raw --languages en-US,en --exclude-generated
```

Options: `--out DIR` (default `raw`), `--languages a,b`, `--exclude-generated`, `--python PATH` (interpreter that has the CLI), `--overwrite`, `--print-text`. It writes UTF-8 with `\n` newlines, drops whitespace-only and consecutively repeated caption lines, names the file after the language code YouTube reports, never overwrites an existing file unless `--overwrite` is given (it adds `.2`, `.3`, … instead), reads the file back to verify it, and prints `saved:`, `language:`, and `format:` lines. Exit codes: `0` saved, `2` no/blocked captions, `3` bad arguments or interpreter problem.

Run one video per invocation with an argument array, not an interpolated shell command. On Windows, prefer this wrapper (or Python `subprocess.run` with `PYTHONIOENCODING=utf-8` and an explicit UTF-8 writer) over PowerShell redirection, whose default encoding mangles non-ASCII text. If the ID starts with `-`, pass the ID as one argument, e.g. `\-abcdefghij`; the wrapper also accepts the URL form.

### Verify before reporting

Require nonempty plain text with at least one non-blank line, and reject error text or placeholder output even when the process exits with code zero. The wrapper already does this. Some versions print a human-readable failure report (`Could not retrieve a transcript…`, `The video is no longer available`) **and still exit 0**, so a non-JSON payload — not the exit code — is the real failure signal. If you invoke the CLI directly, request `--format json`, check the result, require segments with `text`, `start`, and `duration`, and then convert the text yourself instead of saving the JSON (the single video's segment array may be wrapped in an outer array). `--format` accepts `json`, `pretty`, `text`, `webvtt`, and `srt` — there is no Markdown formatter, and JSON must never be the saved deliverable.

Preserve existing files. Reuse a valid existing download unless a refresh is requested; for a requested refresh, save a new numbered filename unless overwrite was explicitly requested. Read back the saved file and report its absolute path, actual language, and format. For multiple URLs, report success/failure per video.

Convert a JSON segment array with:

```python
import json, re
segments = json.loads(raw)
if isinstance(segments, list) and len(segments) == 1 and isinstance(segments[0], list):
    segments = segments[0]
lines = []
for segment in segments:
    text = re.sub(r"\s+", " ", str(segment.get("text", ""))).strip()
    if text and (not lines or lines[-1] != text):
        lines.append(text)
text = "\n".join(lines) + "\n"
```

If YouTube blocks requests (`RequestBlocked`, `IpBlocked`, HTTP 429), report the specific failure without creating an apparent successful download. Use an already-authorized proxy if available; avoid repeated retries after a persistent block. Report disabled/missing subtitles distinctly. Audio transcription is a separate task requiring a user request.

## Brief summary

After downloading and verifying captions, or reusing a valid existing download, read the complete transcript and automatically include a brief summary in the final response. Do not wait for a separate request to summarize. For long transcripts, read in chunks and synthesize across the whole video.

Use the user's conversation language for the summary, independently of the subtitle language. Default to one sentence stating the main point and 3-5 concise takeaways, shorter for simple content. Focus on the central argument, useful conclusions, and only the examples needed to explain them. Base the summary on the transcript; attribute opinions to the speaker and avoid adding unsupported facts or inferring unseen visuals.

Include the verified subtitle file's absolute-path link, actual language, and format alongside the summary. Keep the summary in chat and preserve the original subtitle file unchanged; save a separate summary file only when requested. For multiple videos, provide a brief summary for each successful result.

Honor requests such as download only, no summary, or a different summary length. If retrieval fails and no valid transcript is available, report the failure without inventing a summary. If incomplete or unreadable captions limit the summary, state that limitation.

Project documentation: https://github.com/jdepoix/youtube-transcript-api
