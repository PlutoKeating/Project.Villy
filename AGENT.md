# 工作流程规范 · Agent Constitution

> 本文档定义 Project.Villy 仓库中所有 AI Agent 及人类协作者必须遵守的工作流规范。
> 违反本规范的提交将被要求修正。

---

## 核心原则

### 0. 根目录清洁度

根目录（`Project.Villy/`）**仅允许存在以下文件**：

```
README.md       # 项目总览
AGENT.md        # 本文件
LICENCE         # AGPLv3 许可证
.gitignore      # 根级忽略规则
.gitmodules     # submodule 定义
docs/           # 跨模块文档（架构、路线图）
```

**绝对禁止**将任何模块内部文件（配置、代码、脚本、资源）放置在根目录或 `docs/` 下。每个模块的所有内容严格限定在各自的 `module/` 子目录内。

### 1. 模块化与解耦

- 每个一级子目录（`hardware/`、`firmware/`、`backend/`、`frontend/`、`ros2/`）是一个独立模块
- 模块之间通过 **API 契约** / **文档接口** 而非文件引用耦合
- 每个模块拥有自己的 `README.md`、`.gitignore`、`docs/`、配置文件和源码

### 2. 文档纪律

- **先建脚手架，后填内容** —— 新发现或新成果写入已存在的规范化目录结构中，禁止"一有新内容就开新文件/新目录"
- 所有操作记录按照模块归属写入对应模块的 `docs/` 目录
- 跨模块决策写入根目录 `docs/ARCHITECTURE.md`

### 3. 工程化记录

每一步工作必须记录以下四要素：

| 要素 | 位置 | 要求 |
|------|------|------|
| **发现 / 背景** | 模块 `docs/` | 做了什么、为什么做 |
| **执行方案** | 模块 `docs/` | 完整命令、配置、参数 |
| **执行结果** | 模块 `docs/` | 实际输出、数据、截图 |
| **复盘经验** | 模块 `docs/` | 成功/失败原因、改进方向 |

### 4. Git 规范

- **Commit message 格式**：`<emoji> <模块>: <简短描述>`
  - 示例：`🔧 firmware: 添加 Allwinner R16 交叉编译工具链 submodule`
- **Submodule** 用于引入外部开源工具链，固定到具体 commit
- **禁止提交**：二进制产物、固件镜像、私有凭据、脱敏前的日志

### 5. 外部依赖管理

- 开源工具链 → `git submodule add` 到对应模块的 `submodules/`
- Python 依赖 → `backend/requirements.txt`（固定版本）
- 前端依赖 → `frontend/package.json`
- 系统级依赖 → 在各模块 `docs/` 文档中说明，不在仓库内自动化安装

---

## 模块索引

| 模块 | 职责 | 入口文档 |
|------|------|---------|
| `hardware/` | 硬件逆向、GPIO 映射、协议分析 | `hardware/README.md` |
| `firmware/` | 刷写工具链、镜像构建、刷机记录 | `firmware/README.md` |
| `backend/` | Flask API、HAL 抽象层、认证授权 | `backend/README.md` |
| `frontend/` | React 控制面板、仪表盘 | `frontend/README.md` |
| `ros2/` | ROS 2 集成评估与实现 | `ros2/README.md` |

---

*最后更新：2026-08-08*
