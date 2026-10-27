#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BUNDLE_DIR="$(dirname "$SCRIPT_DIR")"

echo "Validating Risk-Aware CI/CD revision bundle..."

for file in main.py risk_engine.py database_validator.py appspec.yml; do
    if [ ! -f "$BUNDLE_DIR/$file" ]; then
        echo "ERROR: Required file missing: $file"
        exit 1
    fi
done

echo "Validation successful: required files are present."
