from typing import List, Dict

from fastapi import APIRouter

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/tbay",
    tags=["TBayMod"],
    responses={404: {"description": "Not found"}},
)



@router.get("/")
async def is_alive():
    return {"success": True}
