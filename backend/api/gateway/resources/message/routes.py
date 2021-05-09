from fastapi import APIRouter

router = APIRouter()


@router.get("/send")
async def messageSend():
    return {'ok': True}