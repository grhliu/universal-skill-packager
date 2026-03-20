# Universal Skill Packager

将**任何东西**转换为 OpenCode / Claude Code / OpenClaw 标准 Skill：代码、数据、文档、工具、知识库、工作流、Prompts... 万物皆可 Skill！

## 支持的输入类型

| 类型 | 示例 | 输出 Skill |
|------|------|-----------|
| **代码项目** | Python/Node.js/Go 项目 | 可执行 Skill |
| **数据集** | CSV, JSON, Markdown 集合 | 查询 Skill |
| **提示词库** | System prompts, templates | AI 助手 Skill |
| **文档知识** | PDF, 笔记, 手册 | RAG 知识 Skill |
| **工具脚本** | Shell, Python 脚本 | 工具 Skill |
| **工作流** | 自动化流程, 检查清单 | 工作流 Skill |
| **配置集合** | dotfiles, 配置模板 | 配置 Skill |
| **想法/笔记** | Obsidian, Notion 导出 | 知识 Skill |
| **API 集合** | Postman, OpenAPI 规范 | API Skill |
| **任何文件** | 单个文件或文件夹 | 通用 Skill |

## 安装

```bash
# 克隆到 skills 目录
git clone <repo-url> ~/.claude/skills/skill-packager

# 或者本地使用
python scripts/skill_packager.py --interactive
```

## 使用方法

### 交互式模式（推荐）

```bash
python scripts/skill_packager.py --interactive
```

按提示输入：
- 项目路径
- Skill 名称
- 描述、作者、版本
- 自定义命令

### 快速模式

```bash
python scripts/skill_packager.py /path/to/your/project
```

## 生成的 Skill 结构

```
your-skill/
├── skill.yaml          # Skill 配置文件
├── README.md           # 使用说明
├── LICENSE             # MIT 许可证
├── package.json        # 如果是 Node 项目
├── requirements.txt    # 如果是 Python 项目
├── .gitignore
├── main.py             # 入口脚本
├── src/                # 你的源代码
├── scripts/            # 辅助脚本
├── docs/               # 文档
└── templates/          # 模板文件
```

## 使用示例

### 打包代码项目
```bash
# Python 项目
claude /skill-packager create ~/projects/web-scraper

# Node.js 项目  
claude /skill-packager create ~/projects/api-server

# Go 项目
claude /skill-packager create ~/projects/cli-tool
```

### 打包数据和知识
```bash
# Markdown 笔记库
claude /skill-packager create ~/Obsidian/ programming-notes

# CSV 数据集
claude /skill-packager create ~/data/customer-data.csv

# PDF 文档集合
claude /skill-packager create ~/papers/ai-research/
```

### 打包 Prompts 和模板
```bash
# System prompts 集合
claude /skill-packager create ~/prompts/marketing-copy/

# 代码模板
claude /skill-packager create ~/templates/react-components/
```

### 打包工具和工作流
```bash
# Shell 脚本集合
claude /skill-packager create ~/scripts/dev-ops/

# 检查清单
claude /skill-packager create ~/checklists/deploy.md

# 配置文件
claude /skill-packager create ~/dotfiles/
```

### 打包从其他工具导出的内容
```bash
# Notion 导出
claude /skill-packager create ~/Downloads/Notion_Export/

# Postman 集合
claude /skill-packager create ~/apis/postman-collection.json

# Jupyter notebooks
claude /skill-packager create ~/notebooks/data-analysis/
```

## 示例

### 包装 Naval Twin 项目

```bash
python scripts/skill_packager.py --interactive

# 输入：
# Project path: /Users/a1-6/naval_twin
# Skill name: naval-twin
# Description: Naval Ravikant digital twin
# Author: your-name
# Category: ai-assistant
```

生成的 `skill.yaml`：

```yaml
name: naval-twin
description: Naval Ravikant digital twin using NotebookLM + Gemini
version: 1.0.0
author: your-name
category: ai-assistant

commands:
  - name: chat
    description: Chat with Naval
  - name: test
    description: Run Turing tests

entry_points:
  default: main.py
```

## 上传到 GitHub

```bash
cd naval-twin-skill
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/naval-twin-skill.git
git push -u origin main
```

## 在 Claude Code 中使用

```bash
# 加载 Skill
claude skill load naval-twin

# 使用
claude /naval-twin chat
claude /naval-twin test
```

## 支持的項目类型

| 类型 | 自动检测 | 生成的文件 |
|------|---------|-----------|
| Python | ✅ | requirements.txt, main.py |
| Node.js | ✅ | package.json |
| TypeScript | ✅ | package.json, tsconfig.json |
| Go | ✅ | go.mod |
| Rust | ✅ | Cargo.toml |
| Bash | ✅ | Makefile |

## 配置选项

在交互模式下可以配置：

- **name**: Skill 名称（小写，短横线连接）
- **description**: 简短描述
- **version**: 版本号（默认 1.0.0）
- **author**: 作者名
- **category**: 分类（utility, ai-assistant, data-processing 等）
- **commands**: 自定义命令列表
- **requirements**: 依赖列表

## 进阶用法

### 自定义模板

编辑 `templates/` 下的文件：
- `skill.yaml.template` - Skill 配置模板
- `README.md.template` - README 模板
- `main.py.template` - 入口脚本模板

### 批量转换

```bash
for project in ~/projects/*/; do
    python scripts/skill_packager.py "$project"
done
```

## 故障排除

| 问题 | 解决 |
|------|------|
| 无法检测语言 | 手动在 skill.yaml 中指定 |
| Git 初始化失败 | 检查是否已存在 .git 目录 |
| 依赖安装失败 | 手动编辑 requirements.txt |

## License

MIT
