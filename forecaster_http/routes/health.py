from fastapi import APIRouter


router = APIRouter()


@router.get('/')
@router.get('/health')
@router.get('/healthcheck')
async def healthcheck() -> dict:
    return {'status': 'alive'}
