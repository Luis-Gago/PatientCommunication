#!/bin/bash
# Run database migrations

echo "🔄 Running database migrations..."

# Navigate to the paco-api directory
cd "$(dirname "$0")"

# Set PYTHONPATH to ensure app module can be imported
export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}/app"

# Run Alembic upgrade
alembic upgrade head

echo "✅ Migrations complete!"
