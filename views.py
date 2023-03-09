from fastapi import APIRouter, HTTPException, status
from services import GatewayService
from schemas import CreateGateway, StandardOutput, ErrorOutput, GatewayInput

gateway_router = APIRouter()


@gateway_router.post("/create", description="Create gateway", response_model=CreateGateway, responses={201: {"model": StandardOutput}, 400: {"model": ErrorOutput}})
async def create_gateway(gateway: GatewayInput):
    try:
        await GatewayService.create_gateway(gateway=gateway)
        return StandardOutput(message="Gateway created successfully")

    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@gateway_router.get("/list", description="Get all gateways", responses={400: {"model": ErrorOutput}})
async def get_all_gateways():
    try:
        gateways = await GatewayService.get_all_gateways()
        return gateways
    
    except HTTPException as error:
        raise HTTPException(status_code=404, detail='Gateway not found')
    
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

@gateway_router.get("/list/{gateway_id}", description="Get gateway by id", responses={400: {"model": ErrorOutput}})
async def get_gateway_by_id(gateway_id: str):
    try:
        gateway = await GatewayService.get_gateway_by_id(gateway_id=gateway_id)
        return gateway
    
    except HTTPException as error:
        raise HTTPException(status_code=404, detail='Gateway not found')

    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
    
@gateway_router.delete("/delete/{gateway_id}", description="Delete gateway by id", responses={400: {"model": ErrorOutput}})
async def delete_gateway_by_id(gateway_id: str):
    try:
        await GatewayService.delete_gateway_by_id(gateway_id=gateway_id)
        return StandardOutput(message="Gateway deleted successfully")
    
    except HTTPException as error:
        raise HTTPException(status_code=404, detail='Gateway not found')

    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

@gateway_router.put("/update/{gateway_id}", description="Update gateway by id", responses={404: {"model": ErrorOutput}, 400: {"model": ErrorOutput}})
async def update_gateway(gateway_id: str, gateway: GatewayInput):
    try:
        await GatewayService.update_gateway(gateway_id=gateway_id, gateway=gateway)
        return StandardOutput(message="Gateway updated successfully")

    except HTTPException as error:
        raise HTTPException(status_code=404, detail='Gateway not found')

    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
