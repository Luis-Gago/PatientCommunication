from logging.config import fileConfig
from sqlalchemy import engine_from_config, text
from sqlalchemy import pool
from alembic import context
import os
import sys

# Ensure the app module can be imported
# This handles both local development and Railway/production environments
current_dir = os.path.dirname(os.path.abspath(__file__))  # /app/alembic
parent_dir = os.path.dirname(current_dir)  # /app (paco-api root where 'app' module lives)

# Critical: Insert parent directory at position 0 so 'app' module can be found
sys.path.insert(0, parent_dir)

# Also try common Railway paths
for potential_path in ['/app', os.getcwd()]:
    if potential_path not in sys.path and os.path.exists(potential_path):
        sys.path.insert(0, potential_path)

# Debug output for troubleshooting Railway deployment
print(f"DEBUG - Alembic current dir: {current_dir}")
print(f"DEBUG - Parent dir (should contain 'app' module): {parent_dir}")
print(f"DEBUG - Current working directory: {os.getcwd()}")
print(f"DEBUG - sys.path (first 5): {sys.path[:5]}")
print(f"DEBUG - 'app' directory exists at parent_dir: {os.path.exists(os.path.join(parent_dir, 'app'))}")
print(f"DEBUG - PYTHONPATH env: {os.environ.get('PYTHONPATH', 'NOT SET')}")

from app.db.base import Base
from app.models.database import ResearchID, UserSession, DisclaimerAcknowledgment, Conversation
from app.core.config import get_settings

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get database URL from settings
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
