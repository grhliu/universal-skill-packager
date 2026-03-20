#!/usr/bin/env python3
"""
Universal Skill Packager - Main Entry Point
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))


def show_help():
    """Show help message"""
    print("""
Universal Skill Packager
=========================

Usage: claude /skill-packager <command>

Commands:
  create, package    Create a new skill from project
  analyze            Analyze project structure
  help               Show this help

Examples:
  claude /skill-packager create ~/my-project
  claude /skill-packager create ~/my-project -n my-skill
  claude /skill-packager analyze ~/my-project

Or run interactively:
  python scripts/skill_packager.py --interactive
""")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command in ["--help", "-h", "help"]:
        show_help()
    elif command in ["create", "package"]:
        # Import and run packager
        try:
            from skill_packager import main as packager_main

            sys.argv = sys.argv[1:]  # Remove 'skill-packager' from args
            packager_main()
        except ImportError:
            print("Error: Could not import skill_packager module")
            print("Make sure you're running from the skill-packager directory")
    elif command == "analyze":
        print("Analyze command - TODO: implement")
    else:
        print(f"Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()
