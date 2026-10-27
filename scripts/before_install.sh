#!/bin/bash
set -euo pipefail

: "${DEPLOYMENT_GROUP_ID:?Missing CodeDeploy deployment group ID}"
: "${DEPLOYMENT_ID:?Missing CodeDeploy deployment ID}"

ARCHIVE="/opt/codedeploy-agent/deployment-root/${DEPLOYMENT_GROUP_ID}/${DEPLOYMENT_ID}/deployment-archive"

echo "Validating CodeDeploy deployment archive: $ARCHIVE"

if [ ! -d "$ARCHIVE" ]; then
    echo "ERROR: Deployment archive not found."
    exit 1
fi

for file in main.py risk_engine.py database_validator.py appspec.yml; do
    if [ ! -f "$ARCHIVE/$file" ]; then
        echo "ERROR: Required file missing: $file"
        exit 1
    fi
done

echo "Validation successful: required files are present in the deployment archive."
