#!/bin/sh
# Setup local Git hooks for the QuantSmith repo.
# Run this once after cloning the repository.

set -e

ROOT_DIR=$(git rev-parse --show-toplevel)
cd "$ROOT_DIR"

if [ ! -d ".githooks" ]; then
  echo "Error: .githooks directory not found."
  exit 1
fi

chmod +x .githooks/*
git config core.hooksPath .githooks

echo "Git hooks enabled."
