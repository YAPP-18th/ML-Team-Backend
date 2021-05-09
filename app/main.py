import uvicorn

from fastapi  import FastAPI

from app.api  import api_router
from app.core import common_settings


server = FastAPI(title=common_settings.PROJECT_NAME)
server.include_router(api_router, prefix=common_settings.COMMON_API)


if __name__ == "__main__":
    uvicorn.run('app.main:server', host="0.0.0.0", port=8000, reload=True)


