




from fastapi import APIRouter


router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("/search", response_model=SubjectListResponse)
async def search():
    pass