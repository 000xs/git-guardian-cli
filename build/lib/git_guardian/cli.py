# git_guardian/cli.py
# CLI commands handler funcions 
import click
from .scanner import GitGuardianScanner
from .hook_manager import HookManager
from .reporter import Reporter
import sys

#cli function
@click.group()
@click.version_option("1.0.0")
def cli():
    """Git Guardian - Secret Scanner for Git Repositories"""
    pass



#scan function
@cli.command()
@click.argument("path", default=".") #get args data
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
        
#install hook function

@cli.command()
@click.option("--repo-path", default=".", help="Path to repository")
def install_hook(repo_path):
    """Install Git pre-commit hook"""
    HookManager.install_hook(repo_path=repo_path)
    click.echo("🔒 Pre-commit hook activated. Scans will run before each commit.")


if __name__ == "__main__":
    cli()
