from asyncio import run
from api.connection import engine
from api.models import Base


async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    run(init_db())
