# Skills 来源与订阅

来源由用户确认。下列名称对应本地目录及 SKILL.md 的 name；仅跟踪列出的 skills。

## 自建

- `first-principles`
- `learn`
- `xiaohongshu-post`

## 第三方

| 来源 | 已收录 skills | 跟踪分支 | 实际导入 commit | 上游路径与许可证 |
| --- | --- | --- | --- | --- |
| [kunchenguid/gh-axi](https://github.com/kunchenguid/gh-axi) | `gh-axi` | 待确认 | 待确认 | 待确认 |
| [mattpocock/skills](https://github.com/mattpocock/skills/tree/main) | `grill-with-docs`、`improve-codebase-architecture`、`prototype`、`tdd` | `main` | 待确认 | 待确认 |
| [humanlayer/skills](https://github.com/humanlayer/skills) | `show-me` | `main` | `ca7c8088db69e315a8b2deea43820270457f8f3c` | `plugins/show-me/skills/show-me`；MIT（许可证随 skill 保留） |

现有第三方内容的实际导入 commit、上游路径及许可证待核实；首次更新前须核对本地差异并建立版本基线，不能直接覆盖。

## 已知使用限制

- `gh-axi` 需要 Node.js / npx、GitHub CLI 及认证；`xiaohongshu-post` 需要图像生成能力。
- `grill-with-docs` 引用 `grilling`、`domain-modeling`，`improve-codebase-architecture` 引用 `codebase-design`，这些依赖尚未收录。
- `show-me` 的正文可跨 agent 使用；`disable-model-invocation` 与 `agents/openai.yaml` 属于特定 agent 元数据，其他 agent 可能忽略。
- 部分技能含专用工具调用或 agent 元数据，跨 agent 使用时需核实支持情况。
