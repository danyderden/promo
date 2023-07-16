import asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, \
    async_sessionmaker
from sqlalchemy.pool import NullPool

from config import DB_USER_TEST, DB_NAME_TEST, DB_PORT_TEST, DB_HOST_TEST, \
    DB_PASS_TEST
from database import get_async_session
from main import app
from outputter.models import PromoCode

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}" \
                    f"@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False,
                                         class_=AsyncSession)
metadata = PromoCode.metadata
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.rollback()


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope='function', autouse=True)
async def prepare_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
