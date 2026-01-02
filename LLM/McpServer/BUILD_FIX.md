# Build Configuration Fix

## Problem
"Failed to build installable wheels for some pyproject.toml based projects"

## Root Causes
1. Missing or incomplete `pyproject.toml` build system configuration
2. Missing build dependencies (setuptools, wheel)
3. Some packages require compilation (cryptography, etc.) and need build tools
4. Python 3.13 may not have pre-built wheels for all packages yet

## Solutions Implemented

### 1. Created `pyproject.toml`
- Proper `[build-system]` configuration with setuptools backend
- All project metadata and dependencies defined
- Tool configurations for pytest, black, ruff, mypy

### 2. Updated `setup.py`
- Kept for backward compatibility
- Works alongside `pyproject.toml`
- No longer conflicts with build system

### 3. Created Installation Documentation
- `INSTALL.md` with comprehensive troubleshooting
- Platform-specific instructions
- Step-by-step solutions for common issues

### 4. Updated README
- Added reference to installation troubleshooting
- Emphasized upgrading build tools first

## Quick Fix Commands

```bash
# 1. Upgrade build tools (CRITICAL)
pip install --upgrade pip setuptools wheel

# 2. Install problematic packages first (if needed)
pip install --upgrade cffi cryptography

# 3. Install dependencies
pip install -r requirements.txt
```

## Verification

To verify the build configuration works:

```bash
# Test building the package
python -m build

# Or test installation
pip install -e .
```

## For Python 3.13 Users

If you're using Python 3.13 and encounter issues:
1. Some packages may not have wheels yet - they'll need to be built from source
2. Ensure you have build tools installed (Rust for cryptography, C compiler, etc.)
3. Consider using Python 3.12 for better compatibility

## Next Steps

If you still encounter build errors:
1. Check `INSTALL.md` for detailed troubleshooting
2. Identify which specific package is failing
3. Install that package's build dependencies
4. Try installing that package separately first

