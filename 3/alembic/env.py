from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
from app.models import Base  # Импортируйте вашу базу данных (Base)

# Настройки логирования
config = context.config
fileConfig(config.config_file_name)

# Подключение к вашим моделям
target_metadata = Base.metadata

# Асинхронный движок
def get_async_engine():
    return create_async_engine(config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool)

async def run_migrations_online():
    connectable = get_async_engine()

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    raise RuntimeError("Асинхронные миграции поддерживаются только в онлайн-режиме.")
else:
    import asyncio
    asyncio.run(run_migrations_online())
