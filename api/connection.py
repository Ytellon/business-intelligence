from os import getenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATA_BASE_URL = getenv('DATABASE_URL')

engine = create_async_engine(DATA_BASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession)