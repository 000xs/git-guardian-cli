
---

# Git Guardian CLI

**Git Guardian CLI** is a security-focused command-line tool that scans Git repositories for sensitive information like API keys, passwords, and credentials. It helps prevent accidental exposure of secrets before pushing code to remote repositories.

---

## Features

- **Secret Detection**: Uses regex patterns to detect sensitive information in files.
- **Git Hook Integration**: Automatically blocks commits containing exposed secrets.
- **Cross-Platform**: Works on Windows, macOS, and Linux.
- **Custom Rules**: Add your own regex patterns for secret detection.
- **Detailed Reports**: Provides structured output of scan results.
- **Pre-Commit Hook**: Prevents commits with exposed secrets.

---

## Installation

### Prerequisites
- Python 3.7 or higher
- Git

### Install via pip
```bash
pip install git-guardian-cli
```

### Install from Source
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/git-guardian-cli.git
   cd git-guardian-cli
   ```
2. Install the package:
   ```bash
   pip install .
   ```

---

## Usage

### Scan a Repository
To scan a repository for secrets:
```bash
git-guardian scan /path/to/repo
```

#### Options
- `--output` or `-o`: Output format (`cli` or `json`). Default: `cli`.
  ```bash
  git-guardian scan /path/to/repo --output json
  ```

### Install Pre-Commit Hook
To install a pre-commit hook that blocks commits with exposed secrets:
```bash
git-guardian install-hook
```

---

## Configuration

### Custom Rules
You can add custom regex patterns for secret detection by creating a `.gitguardianrc` file in your repository:

```json
{
  "custom_rules": [
    {
      "name": "Custom API Key",
      "pattern": "CUSTOM-[A-Z0-9]{20}"
    }
  ]
}
```

### Ignored Directories
By default, the following directories are ignored during scanning:
- `.git`
- `node_modules`
- `venv`

---

## Examples

### Scan a Repository
```bash
git-guardian scan .
```

### Install Pre-Commit Hook
```bash
git-guardian install-hook
```

### Scan with Custom Rules
1. Create a `.gitguardianrc` file with your custom rules.
2. Run the scan:
   ```bash
   git-guardian scan /path/to/repo
   ```

---

## Development

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/000xs/git-guardian-cli.git
   cd git-guardian-cli
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Run Tests
```bash
python -m pytest tests/ -v
```

### Build the Package
```bash
python setup.py sdist bdist_wheel
```

---

## Contributing

We welcome contributions! Here’s how you can help:

1. **Report Issues**: If you find a bug or have a feature request, open an issue on GitHub.
2. **Submit Pull Requests**: Fork the repository, make your changes, and submit a pull request.
3. **Improve Documentation**: Help us improve the documentation by submitting updates.

Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Why Git Guardian CLI?

- **Prevent Accidental Exposure**: Catch sensitive information before it’s committed.
- **Easy to Use**: Simple CLI commands with detailed reports.
- **Customizable**: Add your own rules for secret detection.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

---

## Support

If you have any questions or need help, please open an issue on [GitHub](https://github.com/000xs/git-guardian-cli/issues).

---

## Acknowledgments

- Built with ❤️ by 000x.
<!-- - Inspired by tools like [truffleHog](https://github.com/trufflesecurity/truffleHog) and [git-secrets](https://github.com/awslabs/git-secrets). -->

---

 