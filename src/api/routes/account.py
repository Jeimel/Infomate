from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def account_details():
    pass
