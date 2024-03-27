from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import postgres_settings as pg

Base = declarative_base()

dsn = f"postgresql+asyncpg://{pg.user}:{pg.password}@{pg.host}:{pg.port}/{pg.db}"

engine = create_async_engine(dsn, echo=pg.echo, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
