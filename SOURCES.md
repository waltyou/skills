# Skills 来源与订阅

来源由用户确认。下列名称对应本地目录及 SKILL.md 的 name；仅跟踪列出的 skills。

## 自建

- `first-principles`
- `learn`
- `xiaohongshu-post`
- `youtube-subtitles`

## 第三方

| 来源 | 已收录 skills | 跟踪分支 | 实际导入 commit | 上游路径与许可证 |
| --- | --- | --- | --- | --- |
| [kunchenguid/gh-axi](https://github.com/kunchenguid/gh-axi) | `gh-axi` | 待确认 | 待确认 | 待确认 |
| [mattpocock/skills](https://github.com/mattpocock/skills/tree/main) | `code-review`、`codebase-design`、`domain-modeling`、`grill-with-docs`、`improve-codebase-architecture`、`prototype`、`retro`、`tdd`、`teach`、`wayfinder` | `main` | 全部为 `d81f3a183412e71a5b1e84ca21bc1a35eea03a60` | 上游路径为 `skills/engineering/<本地目录名>`，`teach` 为 `skills/productivity/teach`；MIT |
| [humanlayer/skills](https://github.com/humanlayer/skills) | `show-me` | `main` | `ca7c8088db69e315a8b2deea43820270457f8f3c` | `plugins/show-me/skills/show-me`；MIT（许可证随 skill 保留） |

表中标为“待确认”的第三方内容，其实际导入 commit、上游路径及许可证仍待核实；首次更新前须核对本地差异并建立版本基线，不能直接覆盖。

`mattpocock/skills` 各 skill 的实际内容已按文件与该来源记录的 commit 逐一核对一致，不再标“待确认”：除 `codebase-design` 目录内附有上游根目录 MIT 许可证副本（版权归 Matt Pocock，上游该技能目录本身不含 LICENSE，更新时予以保留）外，其余文件均与该 commit 逐字节相同。

## 已知使用限制

- `gh-axi` 需要 Node.js / npx、GitHub CLI 及认证；`xiaohongshu-post` 需要图像生成能力。
- `grill-with-docs` 引用的 `domain-modeling` 已收录，引用的 `grilling` 尚未收录；`improve-codebase-architecture` 引用的 `codebase-design`、`domain-modeling`、`prototype` 已收录，引用的 `grilling` 尚未收录。
- `code-review` 与 `wayfinder` 依赖 `setup-matt-pocock-skills` 生成的 `docs/agents/issue-tracker.md`；该技能未收录，缺失时按正文提示运行对应命令，`wayfinder` 退回本地 Markdown 跟踪。
- `retro` 引用的 `writing-for-agents`、`wayfinder` 的 research 票据引用的 `research` 尚未收录；这些技能通过 Skill 工具按名称调用其他 skill，跨 agent 使用需核实该能力。
- `code-review`、`wayfinder` 依赖并行子代理；`wayfinder` 的 research 票据需要子代理与临时分支能力。
- `teach` 与自建 `learn` 都做教学，但形态不同：`teach` 在目标工作区长期积累 `MISSION.md`、`lessons/*.html`、学习记录等文件，`learn` 在对话中按学习目的讲解或自适应教学；需要区分时按调用方式选择。
- `retro`、`teach`、`wayfinder` 带 `disable-model-invocation: true`，只能由用户显式调用；`retro`、`teach`、`wayfinder` 的 `agents/openai.yaml` 另带 `allow_implicit_invocation: false`，属 Codex 元数据，其他 agent 可能忽略。
- `codebase-design` 无外部运行时依赖；`DESIGN-IT-TWICE.md` 流程需要并行子代理能力，并使用目标项目的 `GLOSSARY.md`；`agents/openai.yaml` 是 Codex 元数据，其他 agent 可能忽略。
- `show-me` 的正文可跨 agent 使用；`disable-model-invocation` 与 `agents/openai.yaml` 属于特定 agent 元数据，其他 agent 可能忽略。
- 部分技能含专用工具调用或 agent 元数据，跨 agent 使用时需核实支持情况。
- `youtube-subtitles` 需要 Python 和 `youtube-transcript-api` CLI；正文使用通用命令行，可供具备终端与文件访问能力的 agent 使用。
