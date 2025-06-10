from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine('sqlite+aiosqlite:///database.db')


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
