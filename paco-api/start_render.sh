#!/usr/bin/env bash
# Render startup script for PaCo API

set -o errexit  # Exit on error

echo "=================================="
echo "Starting PaCo API on Render"
echo "=================================="

# Set PYTHONPATH to ensure app module can be imported
export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}$(pwd)"

echo "Working directory: $(pwd)"
echo "PYTHONPATH: $PYTHONPATH"
echo "Python version: $(python --version)"

# Run database migrations
echo "Running Alembic migrations..."
alembic upgrade head

if [ $? -ne 0 ]; then
    echo "ERROR: Database migrations failed"
    exit 1
fi

echo "Migrations completed successfully"
echo "=================================="

# Start the FastAPI application
echo "Starting Uvicorn server on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
