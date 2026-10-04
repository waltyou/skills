---
name: youtube-subtitles
description: Download YouTube subtitles when the user provides a video URL and asks to download or save captions/transcripts (下载字幕). Install or repair the youtube-transcript-api CLI when needed. Default to English, save files under the current workspace's raw directory, and automatically provide a brief summary after a successful download.
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

1. Resolve the active workspace/project root and read applicable local instructions. Default destination is `<workspace>/raw`, never the global skill directory. Create it when a download succeeds. Honor a destination the user explicitly provides.
2. Extract the video ID from `youtube.com/watch?v=...`, `youtu.be/...`, or YouTube `/shorts/`, `/live/`, and `/embed/` URLs. Ignore tracking parameters. Validate an 11-character ID containing letters, digits, `_`, or `-`. Treat a link with both `v` and `list` as one video unless a playlist is requested. This CLI takes IDs, not full URLs.
3. Default language is `en`. Prefer manual English captions, falling back to automatically generated English captions. If `en` is unavailable, list tracks and select an available English variant such as `en-US` or `en-GB`. For an explicit manual-only request use `--exclude-generated`. Never silently substitute another language or auto-translate. If no English track exists, report available languages; translate only when requested.
4. Default format is JSON, preserving text and timestamps. Name the file `<video-id>.<actual-language-code>.json`. Use `srt`, `webvtt`, or `text` with `.srt`, `.vtt`, or `.txt` when requested. Preserve subtitle wording; keep summaries separate.

CLI examples (replace VIDEO_ID):

```sh
python -m youtube_transcript_api VIDEO_ID --languages en --format json
python -m youtube_transcript_api VIDEO_ID --list-transcripts
```

If the ID starts with `-`, prefix it with a literal backslash as documented by the CLI, e.g. `\-abcdefghij`, passed as one argument.

## Write and verify

Run one video per CLI invocation using an argument array, not an interpolated shell command. Capture stdout and stderr before writing. On Windows, prefer Python `subprocess.run` with UTF-8 subprocess output (`PYTHONIOENCODING=utf-8`) and an explicit UTF-8 file writer rather than PowerShell's default redirection encoding.

For JSON, check the process result and parse stdout as JSON. Require a nonempty transcript containing segments with `text`, `start`, and `duration`; reject errors, empty arrays, and malformed output even when the CLI exits with code zero. The CLI JSON formatter may wrap the single video's segment array in an outer array. For other formats check for nonempty, valid subtitle content. Only then save to `raw`.

Preserve existing files. Reuse a valid existing download unless a refresh is requested; for a requested refresh, save a new numbered filename unless overwrite was explicitly requested. Use UTF-8. Read back the saved file to verify it and report its absolute path, actual language, and format. For multiple URLs, report success/failure per video.

If YouTube blocks requests (`RequestBlocked`, `IpBlocked`, HTTP 429), report the specific failure without creating an apparent successful download. Use an already-authorized proxy if available; avoid repeated retries after a persistent block. Report disabled/missing subtitles distinctly. Audio transcription is a separate task requiring a user request.

## Brief summary

After downloading and verifying captions, or reusing a valid existing download, read the complete transcript and automatically include a brief summary in the final response. Do not wait for a separate request to summarize. For long transcripts, read in chunks and synthesize across the whole video.

Use the user's conversation language for the summary, independently of the subtitle language. Default to one sentence stating the main point and 3-5 concise takeaways, shorter for simple content. Focus on the central argument, useful conclusions, and only the examples needed to explain them. Base the summary on the transcript; attribute opinions to the speaker and avoid adding unsupported facts or inferring unseen visuals.

Include the verified subtitle file's absolute-path link, actual language, and format alongside the summary. Keep the summary in chat and preserve the original subtitle file unchanged; save a separate summary file only when requested. For multiple videos, provide a brief summary for each successful result.

Honor requests such as download only, no summary, or a different summary length. If retrieval fails and no valid transcript is available, report the failure without inventing a summary. If incomplete or unreadable captions limit the summary, state that limitation.

Project documentation: https://github.com/jdepoix/youtube-transcript-api
