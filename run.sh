#!/bin/bash

echo "=== Initializing Phase ==="
echo "---> Verifying Authentication"
if [ ! -f "api/client_secret.json" ]; then
  echo "---> Failed to find credentials: api/client_secret.json"
else
  echo "---> Warning!! token.json Not Found..."
  echo "---> Verifying Gmail Account"
  python api/generate_token.py

  if [ ! -f "api/token.json" ]; then
    echo "---> Failed to initialized token"
  else
    echo "---> Successful Initilization"
    echo "---> Running Test"
    pytest tests --headed 
  fi
fi 
