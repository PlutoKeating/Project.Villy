# AGENT.md

> 给专业 Agent 的开发规范。本文件约束所有由 AI Agent 执行的 Project.Villy 项目开发、整理、修复、文档和交付工作。

---

## 1. 开工前强制阅读流程

每一个用户需求开始操刀前，Agent 必须先阅读并理解项目文档。没有完成本节阅读，不得开始修改文件。

### 1.1 必读根目录文档

每次需求开始前必须阅读：

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/ROADMAP.md`

如任务明显涉及启动、环境、部署或本地运行，还必须阅读：

- `AGENT.md`（本文件 — 规范自身）

### 1.2 必读模块文档

如果任务涉及某个一级模块，Agent 必须阅读该模块的入口文档和架构文档。本项目的模块清单：

| 模块 | 职责 | 必读入口 |
|------|------|---------|
| `hardware/` | 硬件逆向、GPIO 映射、协议分析 | `hardware/README.md`、`hardware/docs/` |
| `firmware/` | 刷写工具链、镜像构建、刷机记录 | `firmware/README.md`、`firmware/docs/` |
| `backend/` | Flask API、HAL 抽象层、HMAC 认证 | `backend/README.md`、`backend/docs/` |
| `frontend/` | React 仪表盘、遥控面板 | `frontend/README.md`、`frontend/docs/` |
| `ros2/` | ROS 2 集成评估 | `ros2/README.md`、`ros2/docs/` |

例如：

- 前端任务：阅读 `frontend/README.md`、`frontend/docs/components.md`
- 后端任务：阅读 `backend/README.md`、`backend/docs/api-reference.md`、`backend/docs/auth-scheme.md`
- 硬件任务：阅读 `hardware/README.md`、`hardware/docs/` 下所有相关文档

如任务涉及模块启动、环境变量、脚本或部署，还必须阅读该模块的：

- 配置文件（`backend/config/default.py`、`frontend/package.json`、`frontend/vite.config.ts` 等）
- `.gitignore`（了解模块忽略规则）

如任务涉及容器化或 submodule 操作，还必须阅读：

- `firmware/submodules/` 的 submodule 配置
- `.gitmodules`（若存在）

### 1.3 阅读后的执行要求

Agent 必须把文档中确认的项目结构、API 约定、模块边界、环境变量和已有工作流作为实现约束。不得凭记忆、猜测或通用经验覆盖本项目文档。

与最新的实际源码 / 配置 / 目录树结构相比，**文档缺失、过时或互相矛盾时有发生**，一切信息必须以最新的实际现有代码内容为准。如遇此类情况，Agent 必须先说明冲突，再基于当前代码和用户最新要求做最小必要变更。

---

## 2. 核心职责

Agent 的目标不是"尽快改完"，而是在本地完成可追踪、可回滚、可审查的工程变更。

必须做到：

- 先理解当前仓库结构、现有代码风格、已有文档和用户的最新要求。
- 只修改与任务直接相关的文件，不做无关重构。
- 每次改动后进行必要的本地验证，例如结构检查、类型检查、测试、构建或人工可读核对。
- 在回复用户时说明做了什么、哪些检查通过、哪些检查无法执行以及原因。

### 2.1 工程化记录（四要素）

Project.Villy 是硬件逆向 + 嵌入式开发项目，实验性强。每一步工作必须记录以下四要素：

| 要素 | 位置 | 要求 |
|------|------|------|
| **发现 / 背景** | 模块 `docs/` | 做了什么、为什么做 |
| **执行方案** | 模块 `docs/` | 完整命令、配置、参数 |
| **执行结果** | 模块 `docs/` | 实际输出、数据、截图 |
| **复盘经验** | 模块 `docs/` | 成功 / 失败原因、改进方向 |

### 2.2 模块化与解耦

- 每个一级子目录（`hardware/`、`firmware/`、`backend/`、`frontend/`、`ros2/`）是一个独立模块。
- 模块之间通过 **API 契约 / 文档接口** 而非文件引用耦合。
- 每个模块拥有自己的 `README.md`、`.gitignore`、`docs/`、配置文件和源码。
- **先建脚手架，后填内容** — 新发现写入已存在的规范化目录结构，禁止"一有新内容就开新文件 / 新目录"。

### 2.3 根目录清洁度

根目录（`Project.Villy/`）**仅允许存在以下文件**：

```
README.md       # 项目总览
AGENT.md        # 本文件
LICENCE         # AGPLv3 许可证
.gitignore      # 根级忽略规则
.gitmodules     # submodule 定义（若有）
docs/           # 跨模块文档（架构、路线图）
```

**绝对禁止**将任何模块内部文件（配置、代码、脚本、资源）放置在根目录或 `docs/` 下。每个模块的所有内容严格限定在各自的模块子目录内。

---

## 3. 所有工作或修改必须要与本地 Git 仓库同步

### 3.1 必须本地提交所有变更

对于任何本地文件的修改或增删，**必须全部进行 git 仓库同步检查**，理解是否应当将新增文件添加到 `.gitignore` / `.dockerignore`，或者添加到 commit。

```bash
git diff
git add <changed-files>
git commit -m "<clear local commit message>"
```

执行原则：

- 一个逻辑变更一个提交。
- 文档整理、结构调整、功能修改、修复问题应尽量分开提交。
- **Commit message 格式**：`<emoji> <模块>: <简短描述>`
  - 示例：`🔧 firmware: 添加 Allwinner A33 交叉编译工具链 submodule`
  - 示例：`📝 hardware: 记录 UART 启动日志`
- 提交信息必须说明真实意图，不允许使用 `update`、`fix`、`misc` 这类无法审查的消息。
- 提交前必须检查变更范围，避免把 `.env`、构建产物、依赖目录、缓存、本地数据库等内容纳入提交。
- **禁止提交**：二进制产物、固件镜像、私有凭据、脱敏前的日志。
- 如果当前环境缺少 Git 命令，应明确告知用户，并继续保证文件变更本身可审查。

### 3.2 Submodule 管理

- 开源工具链 → `git submodule add` 到对应模块的 `submodules/`，固定到具体 commit。
- Python 依赖 → `backend/requirements.txt`（固定版本）。
- 前端依赖 → `frontend/package.json`。
- 系统级依赖 → 在各模块 `docs/` 文档中说明，不在仓库内自动化安装。

### 3.3 永远禁止任何 untracked 文件存在

对于任何含有文件改动的工作，必须在工作完成后**立即检查 `git status`**。

必须确保不存在"untracked files"或"uncommitted 且 not-ignored files"。

你需要思考预期之外的 untracked files 的来源，典型的来源是运行 configure 类操作后自动生成的 config 文件，需要你自行判断是否添加到 `.gitignore` 或 commit。

如果存在 **非常确定与你先前工作完全无关的文件改动**，则需要在其他工作全部完成后的最后询问用户如何后续处理。

### 3.4 Agent 高效且谨慎的 push 原则

为方便开发与运维，Agent 可以执行 push 工作，但 **需要遵守以下的 push 规则**：

**其一**，Agent 可以对 **非 main 分支（或：非特定的生产分支）** 执行远程推送命令，包括但不限于：

```bash
git push -u xxx <feature-branch>
```

**其二**，Agent 可以 **在经过用户当下最新的显式授权时（该授权可能在附近的上下文中提出，此时无需询问）** 对 **main 分支（或：特定的生产分支）** 执行远程推送命令，包括但不限于：

```bash
git push
git push -u xxx main
```

**其三**，Agent 严令禁止在 **未二次确认授权时** 执行任何破坏性的远程推送命令，包括但不限于：

```bash
git push --force
git push --force-with-lease
```

原因：

- 远程分支会影响多人协作和发布流水线。
- 推送可能触发 CI/CD、部署、合并规则或生产流程。
- 远程发布权必须由人类开发者或项目维护者控制。

Agent 在本地完成 commit 后，是否 push、何时 push、push 到哪个远程分支，必须由 Human 决定并执行。

再次强调，该 Human 授权在不清晰时需要立即停止工作并询问，在授权清晰时无需询问，直接执行，执行后需要详细汇报 push 工作的细节和涉及范围。

---

## 4. 分支工作流

本项目采用面向多人协作的标准环境流：

```text
personal feature branch → staging branch → production branch
```

Agent 必须默认理解以下含义：

- `feature/<name>` 或个人特性分支：开发和修复的工作区。
- `staging`：集成验证分支，对应预生产或测试环境。
- `production`：生产发布分支，只接受已经验证并批准的变更。

Agent 的工作边界：

- 可以在当前本地分支上修改、暂存、提交。
- 不得自行把变更合并到 `staging` 或 `production`。
- 不得自行创建远程分支或推送远程。
- 如果用户要求涉及 `staging` 或 `production`，必须先说明风险，并只在本地准备变更。

---

## 5. ！！！本地开发规范

### 修改前：

- 完成"开工前强制阅读流程"（第 1 节）。
- 查看相关配置文件、入口文件、类型定义和调用链。
- 确认任务范围，避免误改其他模块。
- 检查当前工作区是否已有用户未提交改动，不得回滚不属于自己的改动。

### 修改中：

- 保持改动小而清晰。
- 复用现有模式和依赖，不轻易引入新框架。
- 不把密钥、令牌、私有地址、个人机器路径写入仓库文档或源码。
- 不提交 `.env` 的真实内容，只维护 `.env.example` 模板（若项目有该文件）。

### 修改后：

- 执行与改动匹配的验证。
- 检查目录结构是否符合项目约定（根目录清洁度、模块隔离）。
- **必须进行依赖列表文件与编译 / 部署等配置文件或脚本的更新**，严格遵循当前代码内容，不要缺失或包含旧内容。
- **必须进行文档更新**，文档范围为全局文档与你修改涉及模块的文档，严格按照你的代码修改与当前最新的代码内容更新文档，不要缺失或包含旧内容。
- **必须进行 git 仓库同步**，本地 `git add` 和 `git commit`，保持审查边界清晰。
- 回复用户时列出文件、验证结果和未完成风险。

---

*最后更新：2026-08-08*
