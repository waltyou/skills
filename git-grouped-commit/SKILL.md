---
name: git-grouped-commit
description: Split a dirty git working tree into a few logically grouped commits. Inspect every change, propose a grouped commit plan with messages, and stage or commit only after the user explicitly approves it. Use when the user asks to 分类提交、分组提交、拆分提交、整理未提交改动, or when many unrelated changes are mixed in one working tree.
---

# Git grouped commit

Turn a pile of unrelated working-tree changes into a small number of coherent, reviewable commits, ordered so that each commit makes sense on its own.

**Hard rule: propose first, execute after approval.** Until the user approves the plan in this conversation, run no `git add`, `git commit`, `git stash`, `git restore`, `git reset`, or `git checkout`. Inspection commands only. This holds even when the grouping looks obvious.

## Scope

One repository at a time. Resolve it with `git rev-parse --show-toplevel` and run commands from there (or pass `-C`). If the workspace holds several repositories, confirm which one before planning.

## 1. Inspect

Read-only, in one batch where possible:

```sh
git status --porcelain=v2 --branch
git diff
git diff --cached
git ls-files --others --exclude-standard
git log --oneline -20
```

Then:

- **Read the actual changes**, not just file names. For large diffs, read per path (`git diff -- <path>`) and identify each hunk's intent. A rename, a moved block, or a formatter pass belongs with what it serves, not with its file type.
- **Learn the local convention**: recent `git log` message style, plus any commit rules in `AGENTS.md`, `CONTRIBUTING.md`, or `docs/`. Follow the repository's existing style.
- **Note dependencies** between changes: a new file and the code that uses it, a schema change and its migration, a lockfile and the manifest change that caused it.
- **Check the starting state**: pre-existing staged changes are the user's own staging intent — plan them as a group (usually first) rather than silently unstaging. Note the current branch; if `HEAD` is detached or the repo is mid-operation (`MERGE_HEAD`, rebase, cherry-pick, bisect), stop and report before planning.

Flag, without committing them:

- credentials and secrets (`.env`, `*.pem`, keys, tokens, connection strings)
- large binaries, generated or vendored output, editor/OS junk
- lockfile or formatting churn that is mechanical rather than intentional
- a single file whose hunks belong to different groups
- unmerged entries (`UU`, `AA`, `DD`) — resolve or ask first

If nothing is changed (or only ignored files are), say so and stop.

## 2. Propose the plan

Answer in the user's language. One group = one intent. Group by what the change accomplishes, never by directory or file extension. Order groups so prerequisites land first and mechanical churn (formatting, renames, version bumps) is separated from behavior changes. Two to six groups is typical; do not invent extra commits for one coherent change.

Output exactly one table plus the details:

| # | 目的 | 文件 | 提交信息 |
| --- | --- | --- | --- |
| 1 | … | `path/a`, `path/b` | `fix(parser): …` |
| 2 | … | `path/c` | `refactor: …` |

Then, for each group: the full message (subject, plus a short body when the reason is not obvious), the files or hunks it covers, and one line on why it is grouped that way. Message style follows the repository history; when history is unclear, use Conventional Commits (`fix:`, `feat:`, `refactor:`, `docs:`, `test:`, `chore:`), imperative mood, subject under ~72 characters, no trailing period. Different formats must not be mixed across the repo's history without reason.

Close the proposal with:

- paths deliberately **left uncommitted**, and why
- flagged items that need a decision (secret, mixed-hunk file, ambiguous rename)
- the exact command sequence you intend to run, briefly
- a direct question: approve as is, or change something

Splitting one file's hunks across groups is possible but needs explicit consent: list the split in the plan and name it as such. Never assume it.

## 3. Wait for approval

Proceed only on a clear go-ahead. An approval that carries edits ("把 A 并进 2，其余照办") is approval of the edited plan: restate the change in one line and execute. Silence, an unrelated reply, or a vague "嗯" is not approval — recap the plan in one line and ask once. Approval covers only the approved plan; if execution reveals that a group must change (a path vanished, a hook rewrote files), stop and re-ask instead of extending scope.

## 4. Execute group by group

For each approved group, in order:

1. Stage exactly the approved paths: `git add -- <path>...`. Never `git add -A`, `git add .`, or `git commit -a`. A deletion is recorded by `git add -- <path>`; confirm with `git status`.
2. Verify the index before committing: `git diff --cached --name-status` must equal the group's paths exactly — nothing missing, nothing from another group. Correct staging with `git restore --staged -- <path>` if needed, never with `git reset --hard` or `git checkout -- .`.
3. Commit with the approved message. Keep multi-line bodies intact (a here-doc via `git commit -F -`, or repeated `-m`). No `--no-verify`, no `--amend` on existing commits, no `--allow-empty` unless the user asked.
4. If a hook blocks the commit: report its output and stop. Do not bypass the hook. If a hook rewrote files (formatter, lint-staged), re-read `git status --short` and tell the user which files moved; re-stage only what belongs to this group, then re-commit.
5. Verify: `git show --stat --oneline HEAD` and `git status --short`. The group's paths must be gone from the pending list and every other change must be untouched.

**Pinpointing hunks in a mixed file:** interactive `git add -p` is usually unavailable to an agent. Preferred order: (a) put the whole file in one group and say so; (b) when the split was explicitly approved, save a backup patch, build the hunk patch for the target group, apply it with `git apply --cached -- <patch>`, verify `git diff --cached` and the remaining `git diff`, and abort the whole group if either does not match.

## 5. Stop conditions

Stop and report instead of improvising when:

- the working tree changed after the plan (other tool, hook, user edit)
- the repo is mid-merge/rebase/cherry-pick/bisect, or unmerged entries appear
- a planned path no longer exists, or the diff no longer matches the plan
- a commit fails for any reason
- the staged content would include a flagged secret, an unexpectedly large file, or another group's work

## Boundaries

- Preserve unrelated work in progress and the user's pre-existing staged state.
- Commit only; do not push, tag, branch, rebase, or rewrite history unless separately asked.
- Do not stash a dirty tree to "clean up" — stash is a history-adjacent change and needs its own approval.
- Do not change git config, install hooks, or touch ignored files.
- Never report a commit as created without the verification output from step 4.

## Final report

List each commit as `<short-hash> <subject>` with its file count, the paths intentionally left uncommitted, and the remaining `git status --short`. If any group was skipped or deferred, say which and why.
