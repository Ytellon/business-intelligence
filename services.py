from sqlalchemy.ext.asyncio.session import async_session
from sqlalchemy.future import select
from sqlalchemy import delete, update
from api.models import Gateway
from schemas import GatewayInput
from api.connection import async_session
from fastapi import HTTPException

class GatewayService:
    async def create_gateway(gateway: GatewayInput):
        async with async_session() as session:
            session.add(Gateway(**gateway.dict()))
            await session.commit()
    
    async def get_all_gateways():
        async with async_session() as session:
            gateways = await session.execute(select(Gateway))
            result = gateways.scalars().all()
            if not result:
                raise HTTPException(status_code=404, detail="Gateways not found")
            return result
    
    async def get_gateway_by_id(gateway_id: str):
        async with async_session() as session:
            gateway = await session.execute(select(Gateway).where(Gateway.gateway_id == gateway_id))
            result = gateway.scalars().first()
            if not result:
                raise HTTPException(status_code=404, detail="Gateway not found")
            return result
        
    async def delete_gateway_by_id(gateway_id: str):
        async with async_session() as session:
            gateway = await session.execute(select(Gateway).where(Gateway.gateway_id == gateway_id))
            result = gateway.scalars().first()
            if not result:
                raise HTTPException(status_code=404, detail="Gateway not found")
            await session.execute(delete(Gateway).where(Gateway.gateway_id == gateway_id))
            await session.commit()
    
    async def update_gateway(gateway_id: str, gateway: GatewayInput):
        async with async_session() as session:
            result = await session.execute(select(Gateway).where(Gateway.gateway_id == gateway_id))
            gateway_exist = result.scalars().first()
            if not gateway_exist:
                raise HTTPException(status_code=404, detail="Gateway not found")
            await session.execute(update(Gateway).where(Gateway.gateway_id == gateway_id).values(**gateway.dict()))
            await session.commit()