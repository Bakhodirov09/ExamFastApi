from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from database import DATABASE_URL  # config.py fayldan database URL import qilyapsiz
from models import Base  # Modellaringizni import qilishni unutmang

# Alembic Config obyekti
config = context.config

# Loggingni sozlash
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# MetaData ni target qiling
target_metadata = Base.metadata

# sqlalchemy.url ni config faylidan qo'lda o'rnatamiz
config.set_main_option('sqlalchemy.url', DATABASE_URL)


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
        config.get_section(config.config_ini_section),
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
