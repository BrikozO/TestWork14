from api import basic_router
from infrastructure.fastapi_cfg import app

app.include_router(basic_router)
