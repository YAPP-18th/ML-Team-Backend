import uvicorn

<<<<<<< HEAD
from fastapi  import FastAPI

<<<<<<< HEAD
from app.api.v1 import api_router
from app.api import user_router
from app.core import settings
=======
from app.api  import api_router
from app.core import common_settings
>>>>>>> 15048eb... 수정: 전체적인 폴더 구조 리팩토링


<<<<<<< HEAD
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(user_router, prefix=settings.API_USER)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
=======
server = FastAPI(title=common_settings.PROJECT_NAME)
server.include_router(api_router, prefix=common_settings.COMMON_API)


if __name__ == "__main__":
    uvicorn.run('app.main:server', host="0.0.0.0", port=8000, reload=True)
>>>>>>> 15048eb... 수정: 전체적인 폴더 구조 리팩토링
=======
from fastapi                   import FastAPI

from app.core   import settings
from app.api.v1 import api_router

server = FastAPI(title=settings.PROJECT_NAME)



server.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run('app.main:server', host="0.0.0.0", port=8000, reload=True)
>>>>>>> 1e939ba... 추가: Study Room
