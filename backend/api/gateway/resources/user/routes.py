from fastapi import APIRouter


router = APIRouter()


@router.get("/profile")
async def userProfile():

    return {'status': True}