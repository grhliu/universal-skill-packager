#!/usr/bin/env python3
"""
Universal Skill Packager - 通用 Skill 打包器
将任何东西转换为 OpenCode / Claude Code / OpenClaw 标准 Skill
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 模板定义
TEMPLATES = {
    "code": {
        "category": "developer-tool",
        "commands": ["run", "test", "config"],
        "entry": "main.py",
        "desc": "Execute {name} tool",
    },
    "knowledge": {
        "category": "knowledge-base",
        "commands": ["query", "search", "add"],
        "entry": "main.py",
        "desc": "Query {name} knowledge base",
    },
    "data": {
        "category": "data-processing",
        "commands": ["analyze", "query", "visualize"],
        "entry": "main.py",
        "desc": "Analyze {name} data",
    },
    "prompt": {
        "category": "ai-assistant",
        "commands": ["list", "use", "category"],
        "entry": "main.py",
        "desc": "Use {name} prompts",
    },
    "tool": {
        "category": "utility",
        "commands": ["exec", "list", "help"],
        "entry": "main.py",
        "desc": "Execute {name} tools",
    },
    "workflow": {
        "category": "automation",
        "commands": ["start", "step", "status"],
        "entry": "main.py",
        "desc": "Run {name} workflow",
    },
    "generic": {
        "category": "utility",
        "commands": ["run", "info"],
        "entry": "main.py",
        "desc": "Access {name}",
    },
}


class SkillPackager:
    """通用 Skill 打包器"""

    def __init__(self, input_path: str, output_dir: str = "."):
        self.input_path = Path(input_path).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.config = {}

    def analyze(self) -> Dict:
        """分析输入类型"""
        if not self.input_path.exists():
            raise FileNotFoundError(f"路径不存在: {self.input_path}")

        analysis = {
            "path": str(self.input_path),
            "is_file": self.input_path.is_file(),
            "is_dir": self.input_path.is_dir(),
            "size": self._get_size(),
            "languages": [],
            "file_types": {},
            "has_readme": False,
            "has_config": False,
            "suggested_type": "generic",
        }

        if self.input_path.is_file():
            analysis.update(self._analyze_file())
        else:
            analysis.update(self._analyze_directory())

        # 确定类型
        analysis["suggested_type"] = self._detect_type(analysis)

        return analysis

    def _analyze_file(self) -> Dict:
        """分析单个文件"""
        ext = self.input_path.suffix.lower()
        size = self.input_path.stat().st_size

        file_types = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".go": "go",
            ".rs": "rust",
            ".java": "java",
            ".sh": "bash",
            ".bash": "bash",
            ".md": "markdown",
            ".txt": "text",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".csv": "csv",
            ".sql": "sql",
            ".html": "html",
            ".css": "css",
        }

        lang = file_types.get(ext, "unknown")

        # 根据文件类型建议 skill 类型
        type_mapping = {
            "python": "code",
            "javascript": "code",
            "typescript": "code",
            "go": "code",
            "rust": "code",
            "java": "code",
            "bash": "tool",
            "markdown": "knowledge",
            "text": "knowledge",
            "json": "data",
            "yaml": "config",
            "csv": "data",
            "sql": "data",
        }

        suggested = type_mapping.get(lang, "generic")

        return {
            "name": self.input_path.stem,
            "extension": ext,
            "language": lang,
            "file_types": {ext: 1},
            "languages": [lang] if lang != "unknown" else [],
            "suggested_type": suggested,
            "is_executable": os.access(self.input_path, os.X_OK)
            or ext in [".py", ".sh"],
        }

    def _analyze_directory(self) -> Dict:
        """分析目录"""
        languages = set()
        file_types = {}
        has_readme = False
        has_config = False

        for item in self.input_path.rglob("*"):
            if item.is_file():
                # 检查 README
                if item.name.lower().startswith("readme"):
                    has_readme = True

                # 检查配置文件
                if item.name in [
                    "package.json",
                    "requirements.txt",
                    "Cargo.toml",
                    "go.mod",
                ]:
                    has_config = True

                # 统计文件类型
                ext = item.suffix.lower()
                file_types[ext] = file_types.get(ext, 0) + 1

                # 检测语言
                lang_map = {
                    ".py": "python",
                    ".js": "javascript",
                    ".ts": "typescript",
                    ".go": "go",
                    ".rs": "rust",
                    ".java": "java",
                    ".sh": "bash",
                }
                if ext in lang_map:
                    languages.add(lang_map[ext])

        # 根据内容判断类型
        suggested = "generic"
        if ".py" in file_types or ".js" in file_types or ".go" in file_types:
            suggested = "code"
        elif ".md" in file_types:
            suggested = "knowledge"
        elif ".csv" in file_types or ".json" in file_types:
            suggested = "data"
        elif ".sh" in file_types:
            suggested = "tool"

        return {
            "name": self.input_path.name,
            "file_count": sum(file_types.values()),
            "file_types": file_types,
            "languages": list(languages),
            "has_readme": has_readme,
            "has_config": has_config,
            "suggested_type": suggested,
        }

    def _get_size(self) -> str:
        """获取可读大小"""
        if self.input_path.is_file():
            size = self.input_path.stat().st_size
        else:
            size = sum(
                f.stat().st_size for f in self.input_path.rglob("*") if f.is_file()
            )

        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def _detect_type(self, analysis: Dict) -> str:
        """智能检测类型"""
        return analysis.get("suggested_type", "generic")

    def create(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: Optional[str] = None,
    ) -> Path:
        """创建 Skill"""

        analysis = self.analyze()

        # 使用提供的参数或自动生成
        self.config = {
            "name": name
            or analysis.get("name", "my-skill")
            .lower()
            .replace(" ", "-")
            .replace("_", "-"),
            "description": description
            or f"Skill generated from {analysis.get('name', 'input')}",
            "version": "1.0.0",
            "author": author or os.getenv("USER", "anonymous"),
            "category": TEMPLATES.get(
                skill_type or analysis["suggested_type"], TEMPLATES["generic"]
            )["category"],
            "type": skill_type or analysis["suggested_type"],
            "analysis": analysis,
        }

        # 创建目录结构
        skill_dir = self.output_dir / f"{self.config['name']}-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)

        # 创建子目录
        for subdir in ["src", "scripts", "docs", "templates"]:
            (skill_dir / subdir).mkdir(exist_ok=True)

        # 生成文件
        self._generate_skill_yaml(skill_dir)
        self._generate_readme(skill_dir)
        self._generate_main(skill_dir)
        self._generate_license(skill_dir)
        self._generate_gitignore(skill_dir)

        # 复制源文件
        self._copy_source(skill_dir)

        # 初始化 git
        self._init_git(skill_dir)

        return skill_dir

    def _generate_skill_yaml(self, skill_dir: Path):
        """生成 skill.yaml"""
        template = TEMPLATES.get(self.config["type"], TEMPLATES["generic"])

        commands_yaml = ""
        for cmd in template["commands"]:
            desc = template["desc"].format(name=self.config["name"])
            if cmd == "run":
                desc = f"Run {self.config['name']}"
            elif cmd == "test":
                desc = f"Test {self.config['name']}"
            commands_yaml += f"  - name: {cmd}\n    description: {desc}\n"

        yaml_content = f"""name: {self.config["name"]}
description: {self.config["description"]}
version: {self.config["version"]}
author: {self.config["author"]}
category: {self.config["category"]}
type: {self.config["type"]}

commands:
{commands_yaml}
entry_points:
  default: main.py
"""

        with open(skill_dir / "skill.yaml", "w") as f:
            f.write(yaml_content)

    def _generate_readme(self, skill_dir: Path):
        """生成 README.md"""
        readme = f"""# {self.config["name"].title()} Skill

{self.config["description"]}

## Installation

```bash
npm install -g {self.config["name"]}-skill
# or
git clone <repo> ~/.claude/skills/{self.config["name"]}
```

## Usage

```bash
claude /{self.config["name"]} --help
claude /{self.config["name"]} run
```

## Commands

- `run` - Run the skill
- `info` - Show info

Generated from: `{self.config["analysis"]["path"]}`

## Author

{self.config["author"]}
"""

        with open(skill_dir / "README.md", "w") as f:
            f.write(readme)

    def _generate_main(self, skill_dir: Path):
        """生成主入口脚本"""
        main_script = f'''#!/usr/bin/env python3
"""
{self.config["name"].title()} Skill - Main Entry Point
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

def main():
    print("{self.config["name"].title()} Skill")
    print("Usage: claude /{self.config["name"]} <command>")
    print("Commands: run, info")

if __name__ == "__main__":
    main()
'''

        with open(skill_dir / "main.py", "w") as f:
            f.write(main_script)
        os.chmod(skill_dir / "main.py", 0o755)

    def _generate_license(self, skill_dir: Path):
        """生成 LICENSE"""
        license_text = f"""MIT License

Copyright (c) {datetime.now().year} {self.config["author"]}

Permission is hereby granted...
"""
        with open(skill_dir / "LICENSE", "w") as f:
            f.write(license_text)

    def _generate_gitignore(self, skill_dir: Path):
        """生成 .gitignore"""
        gitignore = """node_modules/
__pycache__/
.venv/
.env
.DS_Store
*.log
"""
        with open(skill_dir / ".gitignore", "w") as f:
            f.write(gitignore)

    def _copy_source(self, skill_dir: Path):
        """复制源文件到 src/"""
        src_dir = skill_dir / "src"

        if self.input_path.is_file():
            shutil.copy2(self.input_path, src_dir / self.input_path.name)
        else:
            for item in self.input_path.iterdir():
                if item.name.startswith("."):
                    continue
                if item.is_file():
                    shutil.copy2(item, src_dir)
                elif item.is_dir() and item.name not in [
                    ".git",
                    "node_modules",
                    "__pycache__",
                ]:
                    shutil.copytree(item, src_dir / item.name, dirs_exist_ok=True)

    def _init_git(self, skill_dir: Path):
        """初始化 git 仓库"""
        os.chdir(skill_dir)
        os.system("git init > /dev/null 2>&1")
        os.system("git add . > /dev/null 2>&1")
        os.system(f'git commit -m "Initial commit" > /dev/null 2>&1')


def interactive_mode():
    """交互式模式"""
    print("=" * 60)
    print("Universal Skill Packager")
    print("=" * 60)

    input_path = input("\n📁 要打包的路径: ").strip()
    if not os.path.exists(input_path):
        print(f"❌ 路径不存在: {input_path}")
        sys.exit(1)

    print("\n🔍 分析中...")
    packager = SkillPackager(input_path)
    analysis = packager.analyze()

    print(f"类型: {analysis['suggested_type']}")
    print(f"大小: {analysis['size']}")

    name = input(f"\n📝 Skill 名称 [{analysis.get('name', 'my-skill')}]: ").strip()
    if not name:
        name = analysis.get("name", "my-skill")
    name = name.lower().replace(" ", "-").replace("_", "-")

    description = input("📝 描述: ").strip() or f"Skill for {name}"
    author = input("👤 作者: ").strip() or os.getenv("USER", "anonymous")
    output = input("📂 输出目录 [.]: ").strip() or "."

    print(f"\n🔨 创建 {name}...")
    packager = SkillPackager(input_path, output)
    skill_dir = packager.create(name=name, description=description, author=author)

    print(f"\n✅ 完成: {skill_dir}")
    print(f"cd {skill_dir}")
    print(f"claude skill load {name}")


def main():
    parser = argparse.ArgumentParser(description="Universal Skill Packager")
    parser.add_argument("path", nargs="?", help="输入路径")
    parser.add_argument("-n", "--name", help="Skill 名称")
    parser.add_argument("-d", "--description", help="描述")
    parser.add_argument("-a", "--author", help="作者")
    parser.add_argument("-t", "--type", choices=list(TEMPLATES.keys()), help="类型")
    parser.add_argument("-o", "--output", default=".", help="输出目录")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")

    args = parser.parse_args()

    if args.interactive or not args.path:
        interactive_mode()
    else:
        print(f"🔨 打包: {args.path}")
        packager = SkillPackager(args.path, args.output)
        skill_dir = packager.create(
            name=args.name,
            description=args.description,
            author=args.author,
            skill_type=args.type,
        )
        print(f"✅ 完成: {skill_dir}")


if __name__ == "__main__":
    main()
