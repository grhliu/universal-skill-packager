# Universal Skill Packager - 快速上手指南

## 30 秒理解

这个工具能把**任何东西**变成 Claude Code 可用的 Skill：
- ✅ 代码项目 → 可执行工具
- ✅ 笔记/文档 → 知识库  
- ✅ 数据文件 → 查询分析工具
- ✅ Prompts → AI 助手
- ✅ 脚本 → 自动化工具
- ✅ 任何文件/文件夹 → 通用 Skill

## 5 分钟上手

### Step 1: 选择要打包的东西

找任意一个文件夹或文件：
```bash
# 可以是代码项目
~/my-project/

# 可以是笔记
~/Documents/learning-notes/

# 可以是单个文件
~/scripts/backup.sh

# 可以是数据
~/data/sales.csv
```

### Step 2: 运行打包命令

```bash
cd /Users/a1-6/.claude/skills/skill-packager
python3 scripts/skill_packager.py --interactive
```

### Step 3: 按提示输入

```
📁 Project path: /Users/a1-6/naval_twin

📝 Skill name: naval-twin
📝 Description: Naval Ravikant digital twin  
👤 Author: your-name
🏷️ Category: ai-assistant

⚡ Commands:
   name: chat
   desc: Chat with Naval
   
   name: test
   desc: Run tests
   
   [直接回车结束]

📂 Output: ./naval-twin-skill/

✅ Done!
```

### Step 4: 使用你的 Skill

```bash
# 在 Claude Code 中加载
claude skill load naval-twin

# 使用
claude /naval-twin chat
claude /naval-twin test
```

## 实战示例

### 示例 1: 打包学习笔记

**场景**: 你有编程学习笔记，想随时查询

```bash
# 1. 找到笔记目录
ls ~/Obsidian/Python-Notes/
# → 基础语法.md, 面向对象.md, 装饰器.md ...

# 2. 打包
claude /skill-packager create ~/Obsidian/Python-Notes

# 3. 使用
claude /python-notes query "什么是装饰器？"
claude /python-notes search "async"
```

### 示例 2: 打包常用脚本

**场景**: 整理常用脚本，快速执行

```bash
# 1. 收集脚本
mkdir ~/my-scripts
cp ~/scripts/deploy.sh ~/my-scripts/
cp ~/scripts/backup-db.sh ~/my-scripts/
cp ~/scripts/clean-log.sh ~/my-scripts/

# 2. 打包
claude /skill-packager create ~/my-scripts

# 3. 使用
claude /my-scripts deploy
claude /my-scripts backup-db
```

### 示例 3: 打包 Prompt 库

**场景**: 整理收藏的 prompts，快速调用

```bash
# 1. 准备 prompts
cat ~/prompts/copywriting.txt
# → "你是资深文案..."

cat ~/prompts/code-review.txt  
# → "你是代码审查专家..."

# 2. 打包
claude /skill-packager create ~/prompts/

# 3. 使用
claude /prompts list
claude /prompts use copywriting
```

### 示例 4: 打包数据集

**场景**: 让 AI 帮你分析数据

```bash
# 1. 准备数据
ls ~/data/
# → sales-2024.csv

# 2. 打包
claude /skill-packager create ~/data/sales-2024.csv

# 3. 使用
claude /sales-2024 analyze
claude /sales-2024 query "Q4 销售额"
```

### 示例 5: 打包从 Notion 导出的内容

**场景**: 把 Notion 变成可查询的知识库

```bash
# 1. 从 Notion 导出 (Export → Markdown)
# → Notion_Export.zip
unzip Notion_Export.zip -d ~/Notion_Export/

# 2. 打包
claude /skill-packager create ~/Notion_Export/

# 3. 使用
claude /notion-export search "API 设计"
```

## 常见输入类型对照表

| 你有的东西 | 打包命令 | 生成的 Skill |
|-----------|---------|-------------|
| Python 项目 | `create ~/my-tool` | 可执行工具 |
| Markdown 笔记 | `create ~/notes` | 知识查询库 |
| Shell 脚本 | `create ~/scripts` | 命令集合 |
| CSV/JSON 数据 | `create ~/data.csv` | 数据分析工具 |
| System Prompts | `create ~/prompts` | AI 助手库 |
| PDF 文档 | `create ~/papers` | 文档问答 |
| 检查清单 | `create ~/checklist.md` | 交互式清单 |
| API 文档 | `create ~/api-docs` | API 查询工具 |
| 任何文件 | `create ~/anything` | 通用 Skill |

## 进阶技巧

### 批量打包多个项目

```bash
# 打包所有子目录
for dir in ~/projects/*/; do
    claude /skill-packager create "$dir"
done
```

### 自定义配置

在项目中创建 `.skillrc` 文件：

```yaml
name: my-custom-name
category: developer-tool
exclude:
  - node_modules
  - .env
commands:
  run: npm start
  test: npm test
```

打包器会自动读取这些配置。

### 更新已存在的 Skill

```bash
# 增量更新
claude /skill-packager update ~/my-project --skill ./my-project-skill/
```

## 故障排除

### "无法检测项目类型"
```bash
# 手动指定类型
claude /skill-packager create ~/my-folder --type knowledge
# 可选: code, data, knowledge, tool, workflow
```

### "文件太大"
```bash
# 排除大文件
claude /skill-packager create ~/project --exclude "*.mp4,node_modules"
```

### "命令冲突"
```bash
# 在 .skillrc 中自定义命令名
commands:
  deploy-app: ./deploy.sh
  backup-db: ./backup.sh
```

## 下一步

1. ✅ 找个项目试试
2. ✅ 推送到 GitHub 分享
3. ✅ 在 Claude Code 中使用
4. ✅ 迭代优化

---

**核心概念: 任何东西 → Skill → 在 AI 工作流中复用**
