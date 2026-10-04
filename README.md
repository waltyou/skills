# 我的 Skills 与全局指令仓库

管理跨设备、跨 agent 使用的全局 skills 和个人全局指令。项目专用技能与指令随各自项目管理和备份，本仓库不设 projects/global 分类目录。Git 管理内容、历史和备份，agent 根据文档完成导入、更新及本机接入，不需要专用管理 CLI。

每个 skill 在根目录有独立文件夹，包含完整脚本和资料。自建、第三方和自行维护的 fork 在 SOURCES.md 分类。只收录明确希望跨设备同步的内容。

## 用自然语言管理

在本仓库打开 agent，要求它先阅读 [AGENTS.md](AGENTS.md)，然后可以说：

- “从这个仓库收录 review 和 writing，记住我的选择。”
- “检查已订阅 skills 的更新。”
- “更新第三方 skills，保留我的改动，无法判断的迁移集中告诉我。”
- “让这台机器的 Codex、Claude Code、OpenCode 和 pi 使用这份仓库。”
- “同步仓库并检查本机技能是否可用。”

选择和导入版本保存在 [SOURCES.md](SOURCES.md)，以后无需重新选。检查不会自动修改；更新不会订阅上游新出现的 skills；上游删除时保留最后可用版本。

## 新设备

1. 将仓库 clone 到本机选定的位置，各设备可以使用不同目录。
2. 在这个仓库启动 agent，让它阅读 AGENTS.md，核实实际使用产品的全局加载路径，将该目录链接到仓库根目录。
3. 检查发现结果，以及 CLI、MCP、认证等外部依赖。

默认使用整目录链接，例如：

```text
<本机 agent 的全局 skills 加载目录> → <本机仓库根目录>
```

这是接入示意，具体加载路径按 agent 实际版本核实。接入或修复时直接检查本机路径、产品配置及链接目标，不维护本机安装记录文件。链接在各设备分别建立，不随 Git 同步；仓库移动后需重新检查链接。

一次接入后，新增技能无需再建链接。目标加载目录已有内容时，先盘点、处理收录及忽略规则、保留原目录备份，再建立链接，不能直接覆盖。明确不能进入个人仓库的内容留在仓库外。

整目录接入不适用时，可按产品能力使用额外搜索路径或批量逐项链接。不能假定所有 agent 都支持；发现成功不等于工具和元数据跨 agent 兼容，需要实际验证。

## 个人全局指令

| 文件 | 用途 |
| --- | --- |
| [AGENTS.md](AGENTS.md) | 本仓库的管理约定。 |
| [agent-instructions/AGENTS.md](agent-instructions/AGENTS.md) | 供 user level 加载的个人全局指令，包含八条沟通规则、来源说明及共享配置的默认路径。 |

`agent-instructions/` 不是 skill，不包含 SKILL.md。全局指令随本仓库一起保存和同步，正文不依赖特定 agent 的工具或本机绝对路径。

默认以 `~/.agents/AGENTS.md` 作为用户维护全局规则的共享入口。将这个文件链接到仓库内的 `agent-instructions/AGENTS.md` 后，经共享入口编辑会直接更新仓库文件。各 agent 的专用指令文件可仅保留读取共享入口的指引。共享技能入口为 `~/.agents/skills/`。这些是个人配置约定，各产品是否自动读取仍须在接入时核实。

接入全局指令时，可以让 agent：“将这份仓库的 agent-instructions/AGENTS.md 链接到我使用的 agent 的 user level 指令文件，先检查现有内容。”

1. 核实目标产品的指令文件名、加载位置及优先级。下面的路径仅为示意，不代表已验证各产品的兼容性。
2. 检查目标文件及已有链接。已指向正确文件时跳过；已有其他内容时先保留备份并处理差异。
3. 建立指向仓库内全局指令文件的文件符号链接。Windows 的目录 junction 不适用于单个文件。
4. 按产品要求刷新或重启，并核实实际加载结果。只建立链接不能证明指令已生效。

```text
~/.agents/AGENTS.md → <本机仓库根目录>/agent-instructions/AGENTS.md
```

不要将仓库根目录的 AGENTS.md 链接到 user level。各设备单独建立链接；仓库移动后重新检查。通过链接编辑会直接修改仓库内的正文，提交并推送后其他设备才能拉取这些改动。

## 在其他项目对话中新建技能

让 agent 将提炼出的通用技能保存到已链接的全局 skills 目录，文件就直接落在本仓库中；同时要求它读取本仓库 AGENTS.md 并更新 SOURCES.md。无需另行搬运。项目专用技能保留在原项目。

目录链接不会自动将本仓库管理约定传给其他项目的对话，需要在对话中说明，或另行配置各 agent 的全局指令。文件创建后仍须提交、推送才完成远程备份。

## 不希望或不能同步的 skills

- 默认使用 .gitignore：不需要同步的普通技能按具体根目录路径排除，例如 `/company-only/`。提交并推送 .gitignore 后，其他设备也会获得同一规则。示例不代表已创建该忽略项。
- 只有明确属于单台设备的例外才使用 .git/info/exclude；该文件位于本机 Git 内部，不会随仓库同步。日常优先维护 .gitignore 即可。
- 忽略的 skill 仍可能被 agent 加载，只是不进入普通 Git 提交；启停需要使用目标 agent 的配置。不要强制添加排除项。
- 明确不能进入个人仓库的内容保存在仓库外，通过目标产品支持的额外加载方式接入。
- 链接到仓库的 skill 是同一份文件，编辑它会修改仓库。忽略规则不影响已跟踪文件，已推送内容也不会从历史自动消失。
- 只提交明确收录的内容，不自动清理本机技能。拉取时遇到本机忽略目录与上游新增目录同名，先保留并处理冲突。

## 日常同步与备份

- 修改前先同步；工作区干净时可 `git pull --ff-only`，有改动或分叉时让 agent 保留并处理。
- 修改后提交并推送，其他设备再拉取；Git 不会自动同步未提交、未推送的文件。
- 同步个人仓库和更新第三方是两个操作；换机恢复的是已经收录的版本。
- 远程仓库和及时推送提供异地备份。凭据、插件缓存、本机安装状态不入库。
- 整目录接入后，拉取新增和更新的技能无需再建链接。必要时刷新或重启目标 agent。

## 已收录

| Skill | 用途 |
| --- | --- |
| [code-review](code-review/SKILL.md) | 从指定起点审查改动：代码标准与需求规格两轴并行审查。 |
| [codebase-design](codebase-design/SKILL.md) | 深模块设计术语、接口与依赖设计，以及多方案比较。 |
| [domain-modeling](domain-modeling/SKILL.md) | 构建并打磨项目领域模型，维护 GLOSSARY.md 与 ADR。 |
| [first-principles](first-principles/SKILL.md) | 第一性原理分析：分解、假设审计、重组与实验。 |
| [gh-axi](gh-axi/SKILL.md) | 通过 gh-axi CLI 操作 GitHub。 |
| [git-grouped-commit](git-grouped-commit/SKILL.md) | 把工作区改动按意图分组，先提议提交计划，经确认后再分次提交。 |
| [grill-with-docs](grill-with-docs/SKILL.md) | 通过追问完善方案，并整理 ADR 和术语表。 |
| [improve-codebase-architecture](improve-codebase-architecture/SKILL.md) | 分析架构改进机会，生成 HTML 报告并讨论重构方案。 |
| [learn](learn/SKILL.md) | 按学习目的建立简要概览，或通过动态教学发现卡点、补足理解并验证独立迁移。 |
| [prototype](prototype/SKILL.md) | 用临时原型验证逻辑、状态模型或 UI 设计。 |
| [retro](retro/SKILL.md) | 复盘一次编码会话，提出环境与流程改进建议。 |
| [show-me](show-me/SKILL.md) | 用精简图示、代码结构草图与聚焦的 HTML artifact 帮助理解当前主题。 |
| [tdd](tdd/SKILL.md) | 测试驱动开发与测试设计。 |
| [teach](teach/SKILL.md) | 在工作区长期教学，积累课程、参考材料与学习记录。 |
| [wayfinder](wayfinder/SKILL.md) | 把超出单次会话的大工程规划为决策票据地图，逐张推进。 |
| [xiaohongshu-post](xiaohongshu-post/SKILL.md) | 小红书图文策划、配图及发布文案制作。 |
| [youtube-subtitles](youtube-subtitles/SKILL.md) | 下载 YouTube 字幕，默认英文，保存到当前工作区 raw 目录。 |

## License

自有内容采用 [MIT](LICENSE)。第三方内容保留并遵循原始许可证，来源记录在 SOURCES.md。
