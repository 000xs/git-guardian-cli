import os
import re
import argparse
import json
import sys
import subprocess
from pathlib import Path
from git import Repo, InvalidGitRepositoryError
from typing import List, Tuple, Dict
import click  # pip install click

# Enhanced secret patterns with non-capturing groups
SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "AWS Secret Key": r"(?i)aws[_-]?secret[_-]?access[_-]?key[^\n]*[:=][^\n]*",
    "Private Key": r"-----BEGIN (?:RSA|DSA|EC) PRIVATE KEY-----",
    "API Key": r"(?i)api[_-]?key[^\n]*[:=][^\n]*",
    "Database Connection": r"(?:jdbc|mongodb|mysql|postgres|redis|oracle)://[^\"]+",
    "Email Credentials": r"(?i)smtp.+:[^\s]+@[^\s]+",
    "Generic Credentials": r"(?i)(?:password|passwd|pwd)[^\n]*[:=]\s*['\"]?[^\s'\"]{8,}",
}


class GitGuardianScanner:
    def __init__(self, config_path=".gitguardianrc"):
        self.ignored_dirs = [".git", "node_modules", "venv"]
        self.custom_rules = []
        self.config_path = Path(config_path)
        self.load_custom_rules()

    def load_custom_rules(self):
        try:
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    self.custom_rules = json.load(f).get("custom_rules", [])
        except Exception as e:
            print(f"Error loading config: {str(e)}")

    def scan_file(self, file_path: Path) -> List[Tuple[str, str]]:
        findings = []
        try:
            # Skip binary files
            if self.is_binary(file_path):
                return findings
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

                # Check regex patterns
                for secret_type, pattern in {
                    **SECRET_PATTERNS,
                    **{cr["name"]: cr["pattern"] for cr in self.custom_rules},
                }.items():
                    matches = re.findall(pattern, content)
                    if matches:
                        findings.append((secret_type, str(file_path), matches))

                # AI-based check
                if self.ai_scan(content):
                    findings.append(
                        (
                            "AI Detected Secret",
                            str(file_path),
                            ["Potential secret found by AI model"],
                        )
                    )

        except Exception as e:
            click.echo(f"⚠️  Error scanning {file_path}: {str(e)}")
        return findings

    def is_binary(self, file_path: Path) -> bool:
        """Check if a file is binary."""

        try:
            with open(file_path, "rb") as f:
                chunk = f.read(1024)
                if b"\x00" in chunk:  # Null bytes indicate binary file
                    return True
                # Additional check for non-text characters
                if any(byte > 127 for byte in chunk):
                    return True
            return False
        except Exception:
            return False

    def ai_scan(self, content: str) -> bool:
        """Placeholder for AI/ML model integration"""
        # Implement with transformers pipeline in production
        return False

    def scan_repo(self, repo_path: str) -> Dict:
        findings = {}
        try:
            repo = Repo(repo_path)
            changed_files = [item.a_path for item in repo.index.diff(None)] + [
                item.a_path for item in repo.index.diff("HEAD")
            ]

            for root, dirs, files in os.walk(repo_path):
                # Convert to Path object
                root_path = Path(root)
                dirs[:] = [d for d in dirs if d not in self.ignored_dirs]

                for file in files:
                    file_path = root_path / file
                    relative_path = str(file_path.relative_to(repo_path))

                    # Scan all files (not just changed ones)
                    file_findings = self.scan_file(file_path)
                    if file_findings:
                        findings[relative_path] = file_findings

        except InvalidGitRepositoryError:
            click.echo("❌ Not a valid Git repository")
            sys.exit(1)

        return findings


class HookManager:
    @staticmethod
    def install_hook(repo_path: str = ".", hook_type: str = "pre-commit"):
        hook_content = """#!/bin/sh
git-guardian scan --hook
exit $?
        """
        try:
            repo = Repo(repo_path)
            hook_dir = Path(repo.git_dir) / "hooks"
            hook_dir.mkdir(exist_ok=True, parents=True)
            hook_path = hook_dir / hook_type

            hook_path.write_text(hook_content)
            hook_path.chmod(0o755)
            click.echo(f"✅ {hook_type} hook installed successfully")
        except Exception as e:
            click.echo(f"❌ Failed to install hook: {str(e)}")
            raise


class Reporter:
    @staticmethod
    def generate_report(findings: Dict, output_format: str = "cli"):
        if output_format == "json":
            print(json.dumps(findings, indent=2))
        else:
            if not findings:
                click.echo("🎉 No secrets found!")
                return

            click.echo("\n🔍 Scan Results:")
            for file, file_findings in findings.items():
                click.echo(f"\n📂 File: {file}")
                for finding in file_findings:
                    click.echo(f"  🔥 {finding[0]} detected")
                    for match in finding[2]:
                        click.echo(f"    🧩 Match: {match[:50]}...")


@click.group()
@click.version_option("1.0.0")
def cli():
    """Git Guardian - Secret Scanner for Git Repositories"""
    pass


@cli.command()
@click.argument("path", default=".")
@click.option("--output", "-o", default="cli", help="Output format (cli/json)")
def scan(path, output):
    """Scan repository for secrets"""
    scanner = GitGuardianScanner()
    findings = scanner.scan_repo(path)
    Reporter.generate_report(findings, output)

    if findings:
        click.echo("\n❌ Potential secrets found. Commit blocked.")
        sys.exit(1)
    else:
        sys.exit(0)


@cli.command()
@click.option("--repo-path", default=".", help="Path to repository")
def install_hook(repo_path):
    """Install Git pre-commit hook"""
    HookManager.install_hook(repo_path=repo_path)
    click.echo("🔒 Pre-commit hook activated. Scans will run before each commit.")


if __name__ == "__main__":
    cli()
