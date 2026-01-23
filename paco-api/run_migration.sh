#!/bin/bash
# Run database migrations

echo "🔄 Running database migrations..."

# Navigate to the paco-api directory
cd "$(dirname "$0")"

# Run Alembic upgrade
alembic upgrade head

echo "✅ Migrations complete!"
