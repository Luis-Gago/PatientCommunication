#!/bin/bash
# Railway startup script for PaCo backend

# Set working directory
cd /app || exit 1

# Set PYTHONPATH to ensure imports work
export PYTHONPATH=/app:${PYTHONPATH}

# Print debug info
echo "Working directory: $(pwd)"
echo "PYTHONPATH: $PYTHONPATH"
echo "Python version: $(python --version)"
echo "Contents of /app:"
ls -la /app
echo ""
echo "Contents of /app/app:"
ls -la /app/app 2>&1 || echo "app directory not found!"
echo ""
echo "Python can find app module:"
python -c "import sys; sys.path.insert(0, '/app'); from app.models.database import ResearchID; print('✓ YES - app.models.database import successful')" 2>&1 || echo "✗ NO - import failed"
echo ""

# Run database migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Check if migrations succeeded
if [ $? -ne 0 ]; then
    echo "ERROR: Database migrations failed"
    exit 1
fi

echo "Migrations completed successfully"

# Start the FastAPI application
echo "Starting uvicorn server..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
