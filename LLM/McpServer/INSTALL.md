# Installation Guide

## Prerequisites

- Python 3.11 or higher (3.12 recommended)
- pip, setuptools, and wheel (latest versions)
- Build tools for packages that compile C extensions (cryptography, etc.)

## Quick Install

```bash
# 1. Upgrade build tools
pip install --upgrade pip setuptools wheel

# 2. Install dependencies
pip install -r requirements.txt
```

## Troubleshooting "Failed to build installable wheels" Error

If you encounter build errors, follow these steps:

### Step 1: Install/Upgrade Build Tools

```bash
pip install --upgrade pip setuptools wheel build
```

### Step 2: Install System Dependencies

**macOS:**
```bash
brew install openssl rust
export LDFLAGS="-L$(brew --prefix openssl)/lib"
export CPPFLAGS="-I$(brew --prefix openssl)/include"
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev rust cargo
```

**Fedora/RHEL:**
```bash
sudo dnf install gcc openssl-devel libffi-devel python3-devel rust cargo
```

**Windows:**
- Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
- Install [Rust](https://rustup.rs/)

### Step 3: Install Problematic Packages First

Some packages (like `cryptography`) need to be built from source. Install them first:

```bash
# Install cryptography and its dependencies first
pip install --upgrade cffi cryptography

# Then install the rest
pip install -r requirements.txt
```

### Step 4: Use Pre-built Wheels (Preferred)

If available, use pre-built wheels to avoid compilation:

```bash
pip install --only-binary :all: -r requirements.txt
```

If that fails, try installing without the binary-only restriction:

```bash
pip install -r requirements.txt --no-binary cryptography
```

### Step 5: Alternative Installation Methods

**Using conda (if available):**
```bash
conda install -c conda-forge cryptography
pip install -r requirements.txt
```

**Using Docker:**
```bash
docker-compose up -d
```

## Python Version Compatibility

- **Python 3.11**: Fully supported
- **Python 3.12**: Fully supported
- **Python 3.13**: May have issues with some packages that don't have wheels yet

If using Python 3.13, you may need to:
1. Wait for package maintainers to release Python 3.13 wheels
2. Build packages from source (requires build tools)
3. Use Python 3.12 instead

## Development Installation

For development with all dev dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Or install as editable package
pip install -e ".[dev]"
```

## Verify Installation

```bash
# Check if all packages are installed
pip list

# Run tests to verify
pytest tests/

# Try running the server
python -m src.main
```

## Common Issues

### Issue: "error: Microsoft Visual C++ 14.0 or greater is required" (Windows)

**Solution:** Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### Issue: "Failed building wheel for cryptography"

**Solution:**
1. Install Rust: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. Install OpenSSL development libraries
3. Try: `pip install --upgrade pip setuptools wheel cryptography`

### Issue: "No module named '_cffi_backend'"

**Solution:**
```bash
pip install --upgrade cffi
pip install -r requirements.txt
```

### Issue: Packages fail to build on Apple Silicon (M1/M2/M3)

**Solution:**
```bash
# Use Rosetta 2 or install native ARM64 versions
arch -x86_64 pip install -r requirements.txt
# OR
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## Getting Help

If you continue to experience issues:

1. Check Python version: `python --version` (should be 3.11+)
2. Check pip version: `pip --version` (should be 21.0+)
3. Check for error messages in the build output
4. Try installing packages one by one to identify the problematic package
5. Check package-specific installation instructions

