from logging.config import fileConfig
from sqlalchemy import engine_from_config, text
from sqlalchemy import pool
from alembic import context
import os
import sys

# Ensure the app module can be imported
# Try multiple approaches to handle both local and Railway/production environments
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # This is /app (paco-api root)

# Add parent directory first (for Railway/production where we're in /app)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Also ensure current working directory is in path
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

# Debug output for troubleshooting
print(f"DEBUG - Current dir: {current_dir}")
print(f"DEBUG - Parent dir: {parent_dir}")
print(f"DEBUG - CWD: {cwd}")
print(f"DEBUG - sys.path: {sys.path[:3]}")

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
