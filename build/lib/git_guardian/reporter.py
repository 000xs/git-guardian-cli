# git_guardian/reporter.py
import json
import click
from typing import Dict   


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
